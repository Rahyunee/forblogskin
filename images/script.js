(function () {
  "use strict";

  var config = window.tistorySkinConfig || {};
  var root = document.documentElement;

  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn, { once: true });
    } else {
      fn();
    }
  }

  function slugify(text, index) {
    var slug = String(text || "")
      .trim()
      .toLowerCase()
      .replace(/[^\w\u3131-\u318e\uac00-\ud7a3\s-]/g, "")
      .replace(/\s+/g, "-")
      .replace(/-+/g, "-");
    return slug || "section-" + index;
  }

  function uniqueId(base) {
    var id = base;
    var count = 2;
    while (document.getElementById(id)) {
      id = base + "-" + count;
      count += 1;
    }
    return id;
  }

  function initTheme() {
    var saved = localStorage.getItem("tistory-skin-theme");
    if (saved === "light" || saved === "dark") {
      root.setAttribute("data-theme", saved);
    }

    var toggle = document.querySelector("[data-theme-toggle]");
    if (!toggle) return;

    function updateLabel() {
      var current = root.getAttribute("data-theme");
      toggle.textContent = current === "dark" ? "L" : "D";
      toggle.setAttribute("aria-label", current === "dark" ? "라이트모드 전환" : "다크모드 전환");
    }

    toggle.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      localStorage.setItem("tistory-skin-theme", next);
      updateLabel();
    });

    updateLabel();
  }

  function initMenu() {
    var button = document.querySelector("[data-menu-toggle]");
    var nav = document.querySelector("[data-site-nav]");
    if (!button || !nav) return;

    button.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      button.setAttribute("aria-expanded", String(open));
    });

    document.addEventListener("click", function (event) {
      if (!nav.classList.contains("is-open")) return;
      if (nav.contains(event.target) || button.contains(event.target)) return;
      nav.classList.remove("is-open");
      button.setAttribute("aria-expanded", "false");
    });
  }

  function initSearch() {
    var form = document.querySelector("[data-search-form]");
    if (!form) return;

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var input = form.querySelector('input[name="search"]');
      var value = input ? input.value.trim() : "";
      if (!value) return;
      window.location.href = "/search/" + encodeURIComponent(value);
    });
  }

  function initProgress() {
    var bar = document.querySelector(".reading-progress span");
    var article = document.querySelector("[data-article-body]");
    if (!bar || !article) return;

    function update() {
      var rect = article.getBoundingClientRect();
      var total = Math.max(article.offsetHeight - window.innerHeight, 1);
      var read = Math.min(Math.max(-rect.top, 0), total);
      bar.style.width = (read / total) * 100 + "%";
    }

    update();
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
  }

  function initToc() {
    var article = document.querySelector("[data-article-body]");
    var toc = document.querySelector("[data-toc]");
    var tocList = document.querySelector("[data-toc-list]");
    var mobileToc = document.querySelector("[data-mobile-toc]");
    var mobileList = document.querySelector("[data-mobile-toc-list]");
    if (!article || !tocList || !mobileList) return;

    var headings = Array.prototype.slice.call(article.querySelectorAll("h2, h3"));
    if (headings.length < 2) {
      if (toc) toc.classList.add("is-empty");
      var floating = document.querySelector("[data-mobile-toc-toggle]");
      if (floating) floating.hidden = true;
      return;
    }

    var seen = {};
    headings.forEach(function (heading, index) {
      if (!heading.id) {
        var base = slugify(heading.textContent, index + 1);
        heading.id = uniqueId(base);
      } else if (seen[heading.id]) {
        heading.id = uniqueId(heading.id);
      }
      seen[heading.id] = true;

      var li = document.createElement("li");
      li.className = "toc-level-" + heading.tagName.slice(1);
      var link = document.createElement("a");
      link.href = "#" + heading.id;
      link.textContent = heading.textContent.trim();
      li.appendChild(link);
      tocList.appendChild(li);
      mobileList.appendChild(li.cloneNode(true));
    });

    var links = Array.prototype.slice.call(document.querySelectorAll("[data-toc-list] a"));
    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          links.forEach(function (link) {
            link.classList.toggle("is-active", link.getAttribute("href") === "#" + entry.target.id);
          });
        });
      }, { rootMargin: "-20% 0px -70% 0px", threshold: 0.01 });

      headings.forEach(function (heading) {
        observer.observe(heading);
      });
    }

    initMobileToc(mobileToc);
  }

  function initMobileToc(mobileToc) {
    var openButton = document.querySelector("[data-mobile-toc-toggle]");
    var closeButton = document.querySelector("[data-mobile-toc-close]");
    if (!mobileToc || !openButton || !closeButton) return;

    function open() {
      mobileToc.hidden = false;
      document.body.style.overflow = "hidden";
    }

    function close() {
      mobileToc.hidden = true;
      document.body.style.overflow = "";
    }

    openButton.addEventListener("click", open);
    closeButton.addEventListener("click", close);
    mobileToc.addEventListener("click", function (event) {
      if (event.target === mobileToc || event.target.tagName === "A") {
        close();
      }
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !mobileToc.hidden) close();
    });
  }

  function initAdPlaceholders() {
    insertArticleMiddleAd();
    insertListAd();
    hideEmptyAdSlots();
    initMobileStickyAd();
  }

  function hideEmptyAdSlots() {
    if (config.showAdPlaceholders) return;

    Array.prototype.forEach.call(document.querySelectorAll(".ad-slot"), function (slot) {
      if (!slotHasAdContent(slot)) {
        slot.hidden = true;
        slot.setAttribute("aria-hidden", "true");
      }
    });
  }

  function slotHasAdContent(slot) {
    var clone = slot.cloneNode(true);
    Array.prototype.forEach.call(clone.querySelectorAll("span"), function (label) {
      label.remove();
    });

    var text = clone.textContent.replace(/\s+/g, "").trim();
    var hasResolvedText = text && text.indexOf("[##_") === -1;
    var hasAdElement = Boolean(clone.querySelector("ins.adsbygoogle, iframe, script, .kakao_ad_area, [data-ad-client], [data-ad-slot]"));

    return hasResolvedText || hasAdElement;
  }

  function insertArticleMiddleAd() {
    var article = document.querySelector("[data-article-body]");
    var template = document.getElementById("article-middle-ad-template");
    if (!article || !template || article.querySelector('[data-auto-ad="middle"]')) return;

    var afterHeading = Number(config.articleMiddleAdAfterHeading || 2);
    var headings = Array.prototype.slice.call(article.querySelectorAll("h2"));
    var anchor = headings[Math.max(afterHeading - 1, 0)];

    if (!anchor) {
      var paragraphs = Array.prototype.slice.call(article.querySelectorAll("p"));
      anchor = paragraphs[Math.floor(paragraphs.length / 2)];
    }

    if (!anchor || !template.content.firstElementChild) return;

    var node = template.content.firstElementChild.cloneNode(true);
    anchor.insertAdjacentElement("afterend", node);
  }

  function insertListAd() {
    var list = document.querySelector("[data-post-list]");
    var template = document.getElementById("list-ad-template");
    if (!list || !template || list.querySelector('[data-auto-ad="list"]')) return;

    var cards = Array.prototype.slice.call(list.querySelectorAll(".post-card"));
    var index = Number(config.listAdAfterItem || 4) - 1;
    var anchor = cards[index];
    if (!anchor || !template.content.firstElementChild) return;

    anchor.insertAdjacentElement("afterend", template.content.firstElementChild.cloneNode(true));
  }

  function initMobileStickyAd() {
    var wrapper = document.querySelector("[data-mobile-sticky-ad]");
    var closeButton = document.querySelector("[data-mobile-ad-close]");
    if (!wrapper || !config.enableMobileStickyAd) return;

    wrapper.hidden = false;
    if (closeButton) {
      closeButton.addEventListener("click", function () {
        wrapper.hidden = true;
        sessionStorage.setItem("mobile-sticky-ad-closed", "1");
      });
    }

    if (sessionStorage.getItem("mobile-sticky-ad-closed") === "1") {
      wrapper.hidden = true;
    }
  }

  function initThumbnails() {
    normalizePostCardThumbnailMarkup();

    Array.prototype.forEach.call(document.querySelectorAll(".post-card__thumb img, .post-card > img:first-child, .post-card > a:first-child > img"), function (img) {
      img.removeAttribute("width");
      img.removeAttribute("height");

      function markLoaded() {
        if (img.naturalWidth > 0) {
          img.classList.add("is-loaded");
          img.classList.remove("is-broken");
        } else {
          markBroken();
        }
      }

      function markBroken() {
        img.classList.add("is-broken");
        img.classList.remove("is-loaded");
      }

      if (img.complete) {
        markLoaded();
      } else {
        img.addEventListener("load", markLoaded, { once: true });
        img.addEventListener("error", markBroken, { once: true });
      }
    });
  }

  function normalizePostCardThumbnailMarkup() {
    Array.prototype.forEach.call(document.querySelectorAll(".post-card"), function (card) {
      if (card.querySelector(":scope > .post-card__thumb")) return;

      var firstElement = Array.prototype.find.call(card.children, function (child) {
        return child.tagName === "IMG" || child.tagName === "PICTURE" || (child.tagName === "A" && child.querySelector("img, picture"));
      });
      if (!firstElement) return;

      var img = firstElement.tagName === "IMG" ? firstElement : firstElement.querySelector("img");
      if (!img) return;

      var titleLink = card.querySelector(".post-card__body h2 a, h2 a");
      var wrapper = document.createElement("a");
      wrapper.className = "post-card__thumb";
      wrapper.href = (firstElement.tagName === "A" && firstElement.href) || (titleLink && titleLink.href) || "#";
      wrapper.setAttribute("aria-label", (titleLink && titleLink.textContent.trim()) || "대표 이미지");

      img.classList.add("post-card__image");
      wrapper.appendChild(img);
      card.insertBefore(wrapper, card.firstElementChild);

      if (firstElement.parentNode && firstElement !== wrapper && firstElement.childElementCount === 0) {
        firstElement.remove();
      }
    });
  }

  function initArticleEnhancements() {
    var article = document.querySelector("[data-article-body]");
    if (!article) return;

    Array.prototype.forEach.call(article.querySelectorAll("img"), function (img, index) {
      if (index > 0 && !img.hasAttribute("loading")) img.loading = "lazy";
      if (!img.hasAttribute("decoding")) img.decoding = "async";
    });

    Array.prototype.forEach.call(article.querySelectorAll('a[href^="http"]'), function (link) {
      if (link.hostname && link.hostname !== window.location.hostname) {
        link.rel = "nofollow noopener noreferrer";
        link.target = "_blank";
      }
    });
  }

  function initShare() {
    var copyButton = document.querySelector("[data-copy-link]");
    var shareButton = document.querySelector("[data-native-share]");

    if (copyButton) {
      copyButton.addEventListener("click", function () {
        var url = window.location.href;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(function () {
            copyButton.textContent = "복사 완료";
            setTimeout(function () {
              copyButton.textContent = "링크 복사";
            }, 1600);
          });
        } else {
          fallbackCopy(url);
        }
      });
    }

    if (shareButton) {
      shareButton.addEventListener("click", function () {
        if (navigator.share) {
          navigator.share({ title: document.title, url: window.location.href }).catch(function () {});
        } else if (copyButton) {
          copyButton.click();
        }
      });
    }
  }

  function fallbackCopy(text) {
    var textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    textarea.remove();
  }

  ready(function () {
    initTheme();
    initMenu();
    initSearch();
    initProgress();
    initToc();
    initAdPlaceholders();
    initThumbnails();
    initArticleEnhancements();
    initShare();
  });
})();
