(function () {
  "use strict";

  var config = window.sugarcoatConfig || {};
  var afterHeading = Number(config.articleMiddleAdAfterHeading || 2);
  var listAfter = Number(config.listAdAfterItem || 4);
  var showPlaceholders = Boolean(config.showAdPlaceholders);
  var enableSticky = Boolean(config.enableMobileStickyAd);

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
    var n = 2;
    while (document.getElementById(id)) {
      id = base + "-" + n;
      n += 1;
    }
    return id;
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

  function initProgress() {
    var bar = document.querySelector(".reading-progress span");
    var article = document.querySelector("[data-article-body], .post-body");
    if (!bar || !article) return;

    function update() {
      var rect = article.getBoundingClientRect();
      var total = Math.max(article.offsetHeight - window.innerHeight, 1);
      var read = Math.min(Math.max(-rect.top, 0), total);
      bar.style.width = (read / total) * 100 + "%";
    }

    update();
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update, { passive: true });
  }

  function initToc() {
    var article = document.querySelector("[data-article-body], .item-post .post-body");
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
      if (!heading.id) heading.id = uniqueId(slugify(heading.textContent, index + 1));
      else if (seen[heading.id]) heading.id = uniqueId(heading.id);
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

    var links = Array.prototype.slice.call(document.querySelectorAll("[data-toc-list] a, [data-mobile-toc-list] a"));
    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          links.forEach(function (link) {
            link.classList.toggle("is-active", link.getAttribute("href") === "#" + entry.target.id);
          });
        });
      }, { rootMargin: "-18% 0px -72% 0px", threshold: 0.01 });
      headings.forEach(function (heading) { observer.observe(heading); });
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
      if (event.target === mobileToc || event.target.tagName === "A") close();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !mobileToc.hidden) close();
    });
  }

  function cloneTemplateChild(template) {
    if (!template) return null;
    if (template.content && template.content.firstElementChild) {
      return template.content.firstElementChild.cloneNode(true);
    }
    var child = template.querySelector(".ad-slot");
    return child ? child.cloneNode(true) : null;
  }

  function slotHasAdContent(slot) {
    var clone = slot.cloneNode(true);
    Array.prototype.forEach.call(clone.querySelectorAll("span.ad-label, .ad-label"), function (label) {
      label.remove();
    });
    var text = clone.textContent.replace(/\s+/g, "").trim();
    var hasAdElement = Boolean(clone.querySelector("ins.adsbygoogle, iframe, script, [data-ad-client], [data-ad-slot]"));
    return Boolean(text) || hasAdElement;
  }

  function hideEmptyAdSlots() {
    if (showPlaceholders) return;
    Array.prototype.forEach.call(document.querySelectorAll(".ad-slot"), function (slot) {
      if (slot.closest && slot.closest(".ad-template")) return;
      if (slotHasAdContent(slot) || slot.querySelector(".widget, ins.adsbygoogle, iframe")) return;
      slot.hidden = true;
      slot.setAttribute("aria-hidden", "true");
    });
  }

  function adIsFilled(slot) {
    if (slot.querySelector("iframe")) return true;
    var ins = slot.querySelector("ins.adsbygoogle");
    if (!ins) return false;
    return ins.getAttribute("data-ad-status") === "filled";
  }

  function markFilledAdSlot(slot) {
    if (!adIsFilled(slot)) return;
    slot.classList.add("is-filled");
    Array.prototype.forEach.call(slot.querySelectorAll(".ad-label"), function (label) {
      label.hidden = true;
    });
  }

  function watchAdSlots() {
    Array.prototype.forEach.call(document.querySelectorAll(".ad-slot"), function (slot) {
      markFilledAdSlot(slot);
      if (typeof MutationObserver === "undefined") return;
      var observer = new MutationObserver(function () {
        markFilledAdSlot(slot);
      });
      observer.observe(slot, {
        attributes: true,
        childList: true,
        subtree: true,
        attributeFilter: ["data-ad-status", "data-adsbygoogle-status"]
      });
    });
  }

  function widgetPayload(source) {
    if (!source) return null;
    var content = source.querySelector(".widget-content");
    if (content && content.innerHTML.trim()) return content;
    var widget = source.querySelector(".widget.HTML, .widget");
    if (widget && widget.innerHTML.trim()) return widget;
    return null;
  }

  function movePayload(source, target) {
    var payload = widgetPayload(source);
    if (!payload || !target) return false;
    while (payload.firstChild) {
      target.appendChild(payload.firstChild);
    }
    return true;
  }

  function gadgetAlreadyPushed(ins) {
    var sib = ins.nextElementSibling;
    return Boolean(sib && sib.tagName === "SCRIPT" && /adsbygoogle/.test(sib.textContent || ""));
  }

  function activateAdsense(root, force) {
    if (!root) return;
    var nodes = root.querySelectorAll ? root.querySelectorAll("ins.adsbygoogle") : [];
    if (root.matches && root.matches("ins.adsbygoogle")) {
      nodes = [root];
    }
    if (!nodes.length) return;
    window.adsbygoogle = window.adsbygoogle || [];
    Array.prototype.forEach.call(nodes, function (ins) {
      if (ins.closest && ins.closest("#ad-sources, .ad-template")) return;
      var filled = ins.getAttribute("data-ad-status") === "filled" || Boolean(ins.querySelector("iframe"));
      if (filled) return;
      if (!force && gadgetAlreadyPushed(ins)) return;
      if (ins.getAttribute("data-adsbygoogle-status") === "done") {
        ins.removeAttribute("data-adsbygoogle-status");
        ins.removeAttribute("data-ad-status");
        ins.innerHTML = "";
      }
      try {
        window.adsbygoogle.push({});
      } catch (e) {}
    });
  }

  function hasInsertedAutoAd(root, kind) {
    if (!root) return false;
    var nodes = root.querySelectorAll('[data-auto-ad="' + kind + '"]');
    for (var i = 0; i < nodes.length; i += 1) {
      if (!nodes[i].closest || !nodes[i].closest(".ad-template")) return true;
    }
    return false;
  }

  function insertArticleMiddleAd() {
    var article = document.querySelector("[data-article-body], .item-post .post-body");
    var template = document.getElementById("article-middle-ad-template");
    if (!article || !template || hasInsertedAutoAd(article, "middle")) return;

    var headings = Array.prototype.slice.call(article.querySelectorAll("h2"));
    var anchor = headings[Math.max(afterHeading - 1, 0)];
    if (!anchor) {
      var paragraphs = Array.prototype.slice.call(article.querySelectorAll("p"));
      anchor = paragraphs[Math.floor(paragraphs.length / 2)];
    }
    var node = cloneTemplateChild(template);
    if (!anchor || !node) return;
    anchor.insertAdjacentElement("afterend", node);
    activateAdsense(node, true);
  }

  function insertListAd() {
    var list = document.querySelector("[data-post-list], .post-list");
    var template = document.getElementById("list-ad-template");
    if (!list || !template || hasInsertedAutoAd(list, "list")) return;
    var cards = Array.prototype.slice.call(list.querySelectorAll(".post-card, .index-post"));
    var anchor = cards[Math.max(listAfter, 1) - 1];
    var node = cloneTemplateChild(template);
    if (!anchor || !node) return;
    anchor.insertAdjacentElement("afterend", node);
    activateAdsense(node, true);
  }

  function moveBloggerAds() {
    var map = [
      ["ad-article-top", ".ad-slot--article-top"],
      ["ad-list-top", ".ad-slot--list-top"],
      ["ad-list-bottom", ".ad-slot--list-bottom"],
      ["ad-mobile-sticky", ".ad-slot--mobile-sticky"]
    ];

    map.forEach(function (pair) {
      var target = document.querySelector(pair[1]);
      if (movePayload(document.getElementById(pair[0]), target)) {
        activateAdsense(target, true);
      }
    });

    var middleSource = document.getElementById("ad-article-middle");
    var middleTemplate = document.getElementById("article-middle-ad-template");
    fillTemplateSlot(middleSource, middleTemplate);

    var listSource = document.getElementById("ad-list-middle");
    var listTemplate = document.getElementById("list-ad-template");
    fillTemplateSlot(listSource, listTemplate);
  }

  function fillTemplateSlot(source, template) {
    if (!source || !template) return;
    var slot = (template.content && template.content.querySelector(".ad-slot")) || template.querySelector(".ad-slot");
    movePayload(source, slot);
  }

  function initMobileStickyAd() {
    var wrapper = document.querySelector("[data-mobile-sticky-ad]");
    var closeButton = document.querySelector("[data-mobile-ad-close]");
    if (!wrapper || !enableSticky) return;
    wrapper.hidden = false;
    if (sessionStorage.getItem("sugarcoat-sticky-closed") === "1") {
      wrapper.hidden = true;
      return;
    }
    if (closeButton) {
      closeButton.addEventListener("click", function () {
        wrapper.hidden = true;
        sessionStorage.setItem("sugarcoat-sticky-closed", "1");
      });
    }
  }

  function initArticleEnhancements() {
    var article = document.querySelector("[data-article-body], .post-body");
    if (!article) return;

    Array.prototype.forEach.call(article.querySelectorAll("img"), function (img, index) {
      if (index > 0 && !img.hasAttribute("loading")) img.loading = "lazy";
      if (!img.hasAttribute("decoding")) img.decoding = "async";
    });

    Array.prototype.forEach.call(article.querySelectorAll('a[href^="http"]'), function (link) {
      if (link.hostname && link.hostname !== window.location.hostname) {
        link.rel = "noopener noreferrer";
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
        function done() {
          copyButton.textContent = "복사 완료";
          setTimeout(function () { copyButton.textContent = "링크 복사"; }, 1600);
        }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(done).catch(function () {
            fallbackCopy(url);
            done();
          });
        } else {
          fallbackCopy(url);
          done();
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
    try { document.execCommand("copy"); } catch (e) {}
    textarea.remove();
  }

  ready(function () {
    initMenu();
    initProgress();
    initToc();
    moveBloggerAds();
    insertArticleMiddleAd();
    insertListAd();
    hideEmptyAdSlots();
    watchAdSlots();
    initMobileStickyAd();
    initArticleEnhancements();
    initShare();
  });
})();
