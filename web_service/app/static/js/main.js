(async function() {
  'use strict';

  const qs = selector => document.querySelector(selector);
  const qsa = selector => Array.from(document.querySelectorAll(selector));

  let selectedGames = new Set();

  function initSliders() {
    qsa('.content-list').forEach(section => {
      const slider = section.querySelector('.slider');
      const prevBtn = section.querySelector('.slider-nav.prev');
      const nextBtn = section.querySelector('.slider-nav.next');
      prevBtn && prevBtn.addEventListener('click', () => slide(slider, -1));
      nextBtn && nextBtn.addEventListener('click', () => slide(slider, 1));
    });
  }

  function slide(slider, direction) {
    const scrollAmount = slider.clientWidth;
    slider.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' });
  }

  function initSelection() {
    qsa('.item').forEach(item => {
      item.addEventListener('click', () => toggleSelect(item));
    });
  }

  function toggleSelect(item) {
    const appid = item.dataset.appid;
    if (selectedGames.has(appid)) {
      selectedGames.delete(appid);
      item.classList.remove('selected');
    } else if (selectedGames.size < 3) {
      selectedGames.add(appid);
      item.classList.add('selected');
    }
    updateSubmitButton();
  }

  function updateSubmitButton() {
    const btn = qs('#submit-button');
    btn.disabled = selectedGames.size !== 3;
    sessionStorage.setItem('game_list', JSON.stringify({ game_list: [...selectedGames] }));
  }

  function bindSubmit() {
    const btn = qs('#submit-button');
    btn.addEventListener('click', () => {
      if (!btn.disabled) window.location.href = '/recommendation/';
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initSliders();
    initSelection();
    bindSubmit();
  });
})();