// customersearch.js - robust, defensive autocomplete + global search + clear
(function () {
  document.addEventListener('DOMContentLoaded', function () {

    // Try multiple possible IDs so this file can be reused across pages
    const input = document.getElementById('customerNameInput') || document.getElementById('globalSearchInput') || null;
    const suggestionBox = document.getElementById('customerNameSuggestions') || document.getElementById('globalSuggestions') || null;
    const searchButton = document.getElementById('searchButton') || document.getElementById('globalSearchButton') || null;
    const clearButton = document.getElementById('clearButton') || document.getElementById('globalClearButton') || null;
    const categorySelect = document.getElementById('categorySelect') || null;
    const statusSelect = document.getElementById('statusSelect') || null;

    console.log('customersearch.js loaded');

    // Suggestion API URL from template (must be set in HTML before loading this file)
    if (typeof CUSTOMER_SUGGEST_URL === 'undefined' || !CUSTOMER_SUGGEST_URL) {
      window.CUSTOMER_SUGGEST_URL = '/ajserp/customers/suggest-name/';
      console.warn('CUSTOMER_SUGGEST_URL not defined — using fallback:', window.CUSTOMER_SUGGEST_URL);
    } else {
      window.CUSTOMER_SUGGEST_URL = CUSTOMER_SUGGEST_URL;
    }

    // Redirect URL after clear — set per page in template: const CLEAR_REDIRECT_URL = "{% url 'ajserp:customers' %}";
    if (typeof CLEAR_REDIRECT_URL === 'undefined' || !CLEAR_REDIRECT_URL) {
      window.CLEAR_REDIRECT_URL = null; // fallback to pathname later
    } else {
      window.CLEAR_REDIRECT_URL = CLEAR_REDIRECT_URL;
    }

    // Helper: safe no-op if required DOM not present
    if (!input || !suggestionBox) {
      console.warn('customersearch.js: optional elements missing. input:', !!input, 'suggestionBox:', !!suggestionBox);
      // We continue because search/clear might still be needed (buttons could exist)
    }

    // Utility: escape HTML
    function escapeHtml(s) {
      return (s || '').replace(/[&<>"]/g, function (c) {
        return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];
      });
    }

    // Render suggestion list (safe if suggestionBox null)
    function showSuggestions(list) {
      if (!suggestionBox) return;
      suggestionBox.innerHTML = '';
      if (!Array.isArray(list) || list.length === 0) {
        suggestionBox.style.display = 'none';
        return;
      }
      list.forEach(item => {
        const a = document.createElement('a');
        a.href = '#';
        a.className = 'list-group-item list-group-item-action';
        a.style.cursor = 'pointer';
        a.innerHTML = `<div><strong>${escapeHtml(item.name)}</strong></div>` +
                      (item.contact ? `<div class="small text-muted">${escapeHtml(item.contact)}</div>` : '');
        a.dataset.name = item.name || '';
        a.dataset.id = item.id || '';
        a.addEventListener('click', function (e) {
          e.preventDefault();
          if (input) {
            input.value = this.dataset.name;
          }
          if (suggestionBox) suggestionBox.style.display = 'none';
        });
        suggestionBox.appendChild(a);
      });
      suggestionBox.style.display = 'block';
    }

    // Debounce helper
    function debounce(fn, wait) {
      let t = null;
      return function () {
        const args = arguments;
        clearTimeout(t);
        t = setTimeout(() => fn.apply(this, args), wait);
      };
    }

    // Fetch suggestions via API
    async function fetchSuggestions(q) {
      if (!q) {
        showSuggestions([]);
        return;
      }
      const url = `${window.CUSTOMER_SUGGEST_URL}?q=${encodeURIComponent(q)}`;
      try {
        const resp = await fetch(url, { credentials: 'same-origin' });
        if (!resp.ok) {
          console.warn('suggestions API responded with', resp.status);
          showSuggestions([]);
          return;
        }
        const data = await resp.json();
        showSuggestions(Array.isArray(data.results) ? data.results : []);
      } catch (err) {
        console.error('fetchSuggestions error', err);
        showSuggestions([]);
      }
    }

    const debouncedFetch = debounce(fetchSuggestions, 200);

    // Input events (only if input exists)
    if (input) {
      input.addEventListener('input', function () {
        const q = (input.value || '').trim();
        if (!q) {
          if (suggestionBox) suggestionBox.style.display = 'none';
          return;
        }
        debouncedFetch(q);
      });

      // keyboard nav
      input.addEventListener('keydown', function (e) {
        if (!suggestionBox || suggestionBox.style.display !== 'block') return;
        const items = Array.from(suggestionBox.querySelectorAll('.list-group-item'));
        if (!items.length) return;
        const active = suggestionBox.querySelector('.active');
        let idx = items.indexOf(active);
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          if (active) active.classList.remove('active');
          idx = Math.min(items.length - 1, idx + 1);
          items[idx].classList.add('active');
          items[idx].scrollIntoView({ block: 'nearest' });
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          if (active) active.classList.remove('active');
          idx = Math.max(0, idx - 1);
          items[idx].classList.add('active');
          items[idx].scrollIntoView({ block: 'nearest' });
        } else if (e.key === 'Enter') {
          e.preventDefault();
          const sel = suggestionBox.querySelector('.active') || items[0];
          if (sel) sel.click();
        }
      });
    }

    // Hide suggestion box when clicking outside
    document.addEventListener('click', function (e) {
      if (suggestionBox && input && !suggestionBox.contains(e.target) && e.target !== input) {
        suggestionBox.style.display = 'none';
      }
    });

    // Helper: perform search by setting ?q=... and preserving other filters (category/status)
    function doSearchAndNavigate(qValue) {
      const url = new URL(window.location.href);
      // set q
      url.searchParams.set('q', qValue || '');
      // preserve category/status if present on page
      if (categorySelect) {
        if (categorySelect.value) url.searchParams.set('category', categorySelect.value);
        else url.searchParams.delete('category');
      }
      if (statusSelect) {
        if (statusSelect.value) url.searchParams.set('status', statusSelect.value);
        else url.searchParams.delete('status');
      }
      window.location.href = url.toString();
    }

    // Search button (if exists) triggers global search 'q'
    if (searchButton) {
      searchButton.addEventListener('click', function () {
        const qValue = input ? (input.value || '').trim() : '';
        doSearchAndNavigate(qValue);
      });
    }

    // Pressing Enter in the input should trigger search (if not selecting suggestion)
    if (input) {
      input.addEventListener('keyup', function (e) {
        if (e.key === 'Enter') {
          // if suggestion visible and an active item exists, let keyboard handler handle it
          if (suggestionBox && suggestionBox.style.display === 'block' && suggestionBox.querySelector('.active')) {
            // handled by keydown handler
            return;
          }
          // otherwise perform search
          const qValue = (input.value || '').trim();
          doSearchAndNavigate(qValue);
        }
      });
    }

    // Clear button resets inputs and redirects to per-page CLEAR_REDIRECT_URL (if provided in template),
    // otherwise falls back to pathname (removes all query params)
    if (clearButton) {
      clearButton.addEventListener('click', function () {
        // clear visible inputs
        if (input) input.value = '';
        if (categorySelect) categorySelect.value = '';
        if (statusSelect) statusSelect.value = '';
        if (suggestionBox) suggestionBox.style.display = 'none';

        // Redirect to page-specific URL if provided, else to pathname
        if (window.CLEAR_REDIRECT_URL) {
          window.location.href = window.CLEAR_REDIRECT_URL;
        } else {
          // remove query params
          window.location.href = window.location.pathname;
        }
      });
    }

    // Expose debug helpers (optional)
    window.__customerSearch = {
      fetchSuggestions,
      showSuggestions,
      doSearchAndNavigate
    };

    console.log('customersearch.js initialized');

  }); // DOMContentLoaded
})(); // IIFE
