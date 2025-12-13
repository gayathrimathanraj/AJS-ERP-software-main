/* estimatesearch.js - select fills input only (no auto-submit) */
(function () {
  'use strict';

  const ENDPOINTS = {
    estimate: '/ajserp/api/get-estimate-suggestions/?q=',
    customer: '/ajserp/api/get-customer-suggestions/?q=',
    global: '/ajserp/api/get-global-suggestions/?q='
  };

  const estimateInput = document.getElementById('estimateNumberInput') || document.getElementById('orderNumberInput');
  const estimateBox = document.getElementById('estimateNumberSuggestions') || document.getElementById('orderNumberSuggestions');

  const customerInput = document.getElementById('customerNameInput');
  const customerBox = document.getElementById('customerNameSuggestions');

  const globalInput = document.getElementById('globalSearchInput');
  const globalBox = document.getElementById('globalSuggestions');

  const filterForm = document.getElementById('filterForm');
  // optional search button (if you have a button with id 'searchButton' you can detect clicks)
  const searchButton = document.getElementById('searchButton');

  function debounce(fn, wait = 200) {
    let t = null;
    return function () {
      const args = arguments;
      clearTimeout(t);
      t = setTimeout(() => fn.apply(this, args), wait);
    };
  }

  function normalizeResponse(data) {
    if (!data) return [];
    if (Array.isArray(data)) return data;
    if (Array.isArray(data.results)) return data.results;
    return [];
  }

  function renderSuggestions(box, suggestions) {
    if (!box) return;
    if (!Array.isArray(suggestions) || suggestions.length === 0) {
      box.style.display = 'none';
      box.innerHTML = '';
      return;
    }

    let html = '';
    suggestions.forEach(item => {
      const value = (item.value ?? item.name ?? item.estimate_number ?? '').toString().replace(/'/g, "\\'");
      const text = (item.text ?? item.name ?? value).toString();
      html += `<a href="#" class="list-group-item list-group-item-action suggestion-item" data-value="${value}">${escapeHtml(text)}</a>`;
    });

    box.innerHTML = html;
    box.style.display = 'block';
  }

  function escapeHtml(s) {
    return String(s || '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  }

  async function fetchAndShow(endpoint, q, box) {
    if (!box) return;
    if (!q || String(q).trim().length === 0) {
      box.style.display = 'none';
      box.innerHTML = '';
      return;
    }
    const url = endpoint + encodeURIComponent(q);
    try {
      const resp = await fetch(url, { credentials: 'same-origin' });
      if (!resp.ok) {
        renderSuggestions(box, []);
        return;
      }
      const data = await resp.json();
      const list = normalizeResponse(data);
      renderSuggestions(box, list);
    } catch (err) {
      console.error('Autocomplete fetch error', err);
      renderSuggestions(box, []);
    }
  }

  const debouncedEstimate = debounce(q => fetchAndShow(ENDPOINTS.estimate, q, estimateBox), 160);
  const debouncedCustomer = debounce(q => fetchAndShow(ENDPOINTS.customer, q, customerBox), 160);
  const debouncedGlobal = debounce(q => fetchAndShow(ENDPOINTS.global, q, globalBox), 160);

  function attachSuggestionClickHandler(box, onSelect) {
    if (!box) return;
    box.addEventListener('click', function (ev) {
      ev.preventDefault();
      const item = ev.target.closest('.suggestion-item');
      if (!item) return;
      const value = item.dataset.value;
      onSelect && onSelect(value);
      box.style.display = 'none';
    });
  }

  // NEW: selection behavior -> only fill the input, do NOT auto-submit
  function selectSuggestionByType(type, value) {
    if (!type) return;
    if (type === 'estimate') {
      const input = estimateInput || document.getElementById('estimateNumberInput') || document.getElementById('orderNumberInput');
      if (input) {
        input.value = value;
        input.focus();                 // focus helps user to confirm/witness
        input.setAttribute('data-selected', 'true'); // optional flag if you want to check later
      }
      // DO NOT submit form here — user must click Search
    } else if (type === 'customer') {
      const input = customerInput || document.getElementById('customerNameInput');
      if (input) {
        input.value = value;
        input.focus();
        input.setAttribute('data-selected', 'true');
      }
      // DO NOT submit
    } else if (type === 'global') {
      const input = globalInput || document.getElementById('globalSearchInput');
      if (input) {
        input.value = value;
        input.focus();
        input.setAttribute('data-selected', 'true');
      }
      // DO NOT navigate automatically — keep behavior consistent
    }
  }

  attachSuggestionClickHandler(estimateBox, value => selectSuggestionByType('estimate', value));
  attachSuggestionClickHandler(customerBox, value => selectSuggestionByType('customer', value));
  attachSuggestionClickHandler(globalBox, value => selectSuggestionByType('global', value));

  // hide on outside click
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.list-group') && !e.target.classList.contains('form-control')) {
      if (estimateBox) estimateBox.style.display = 'none';
      if (customerBox) customerBox.style.display = 'none';
      if (globalBox) globalBox.style.display = 'none';
    }
  });

  // inputs => fetch suggestions
  if (estimateInput) {
    estimateInput.addEventListener('input', function () {
      debouncedEstimate(this.value);
      // clear any 'selected' flag
      this.removeAttribute('data-selected');
    });
    // keep Enter behavior if desired (pressing Enter submits)
    estimateInput.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') {
        ev.preventDefault();
        if (filterForm) filterForm.submit();
      }
    });
  }

  if (customerInput) {
    customerInput.addEventListener('input', function () {
      debouncedCustomer(this.value);
      this.removeAttribute('data-selected');
    });
    customerInput.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') {
        ev.preventDefault();
        if (filterForm) filterForm.submit();
      }
    });
  }

  if (globalInput) {
    globalInput.addEventListener('input', function () {
      debouncedGlobal(this.value);
      this.removeAttribute('data-selected');
    });
    globalInput.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') {
        ev.preventDefault();
        const q = (this.value || '').trim();
        if (q) window.location.href = `${window.location.pathname}?q=${encodeURIComponent(q)}`;
      }
    });
  }

  // Optional: if you have a dedicated search button, ensure it submits the form (or performs expected action)
  if (searchButton) {
    searchButton.addEventListener('click', function (e) {
      e.preventDefault();
      if (filterForm) filterForm.submit();
    });
  }

  // Backwards-compatibility wrapper in case old inline calls exist
  window.estimateSelectSuggestion = function (type, value) {
    // map old names to our types
    if (type === 'estimateNumber' || type === 'orderNumber') type = 'estimate';
    selectSuggestionByType(type, value);
  };

  window.__estimateSearch = {
    select: selectSuggestionByType,
    fetchAndShow
  };

  console.log('estimatesearch.js ready — suggestions fill inputs only (no auto-submit).');

})(); // IIFE
