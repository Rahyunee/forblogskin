#!/usr/bin/env node
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
  const result = {
    templateTag: window.document.getElementById("article-middle-ad-template").tagName,
    middleInsertedAfter: h2s[1] && h2s[1].nextElementSibling === middle ? h2s[1].textContent.trim() : null,
    listInsertedAfter: cards[3] && cards[3].nextElementSibling === listAd ? cards[3].querySelector("h2").textContent.trim() : null,
    tocCount: window.document.querySelectorAll("[data-toc-list] li").length,
  };
  console.log(JSON.stringify(result, null, 2));
  if (!result.middleInsertedAfter || !result.listInsertedAfter || result.tocCount < 2) {
    process.exit(1);
  }
});
