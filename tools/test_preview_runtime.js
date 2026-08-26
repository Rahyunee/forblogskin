#!/usr/bin/env node
try {
  require.resolve("jsdom");
} catch (err) {
  console.error("jsdom is required: npm install jsdom");
  process.exit(1);
}
const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");

const root = path.resolve(__dirname, "..");
const html = fs.readFileSync(path.join(root, "preview.html"), "utf8")
  .replace('<script src="./script.js" defer></script>', "");
const script = fs.readFileSync(path.join(root, "script.js"), "utf8");

const dom = new JSDOM(html, {
  url: "file:///workspace/preview.html",
  runScripts: "dangerously",
  pretendToBeVisual: true,
});
const { window } = dom;
window.sugarcoatConfig = {
  articleMiddleAdAfterHeading: 2,
  listAdAfterItem: 4,
  showAdPlaceholders: true,
  enableMobileStickyAd: false,
};
window.adsbygoogle = [];
window.eval(script);

function waitReady() {
  if (window.document.readyState !== "loading") return Promise.resolve();
  return new Promise((resolve) => {
    window.document.addEventListener("DOMContentLoaded", resolve, { once: true });
  });
}

waitReady().then(() => {
  const article = window.document.querySelector("[data-article-body]");
  const list = window.document.querySelector(".post-list");
  const h2s = [...article.querySelectorAll("h2")];
  const cards = [...list.querySelectorAll(".post-card")];
  const middle = article.querySelector('[data-auto-ad="middle"]');
  const listAd = list.querySelector('[data-auto-ad="list"]');
  const bottom = window.document.querySelector(".ad-slot--article-bottom");
  const sidebar = window.document.querySelector(".ad-slot--sidebar");
  const result = {
    templateTag: window.document.getElementById("article-middle-ad-template").tagName,
    middleInsertedAfter: h2s[1] && h2s[1].nextElementSibling === middle ? h2s[1].textContent.trim() : null,
    listInsertedAfter: cards[3] && cards[3].nextElementSibling === listAd ? cards[3].querySelector("h2").textContent.trim() : null,
    tocCount: window.document.querySelectorAll("[data-toc-list] li").length,
    bottomHasAd: Boolean(bottom && bottom.querySelector('ins[data-ad-slot="1008345394"]')),
    sidebarHasAd: Boolean(sidebar && sidebar.querySelector('ins[data-ad-slot="7633913202"]')),
    hiddenSourceEmpty: !window.document.querySelector("#ad-article-bottom .widget-content ins"),
    adsPushed: window.adsbygoogle.length,
    bottomLabelHidden: Boolean(bottom && bottom.classList.contains("has-ad")),
  };
  console.log(JSON.stringify(result, null, 2));
  if (!result.middleInsertedAfter || !result.listInsertedAfter || result.tocCount < 2) {
    process.exit(1);
  }
  if (!result.bottomHasAd || !result.sidebarHasAd || !result.hiddenSourceEmpty || result.adsPushed < 2 || !result.bottomLabelHidden) {
    process.exit(1);
  }
});
