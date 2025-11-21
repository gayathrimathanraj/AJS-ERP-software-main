// CUSTOMER RECEIPT JAVASCRIPT - COMPLETE VERSION WITH DEBUG (FIXED)
document.addEventListener('DOMContentLoaded', function() {
    console.log('🧾 Customer Receipt JavaScript loaded');
    initializeCustomerReceipt();
});

function initializeCustomerReceipt() {
    console.log('🚀 Initializing Customer Receipt...');
    
    const customerSearchInput = document.getElementById('customerCode');
    if (customerSearchInput) {
        customerSearchInput.addEventListener('input', handleCustomerSearch);
        console.log('✅ Customer receipt search input initialized');
    } else {
        console.log('❌ Customer receipt search input not found');
        return;
    }

    const amountCollectedInput = document.getElementById('amountCollected');
    if (amountCollectedInput) {
        amountCollectedInput.addEventListener('input', calculateCustomerBalance); // ← CHANGED
        console.log('✅ Amount collected input initialized');
    }

    const paymentMethodInput = document.getElementById('paymentMethod');
    if (paymentMethodInput) {
        paymentMethodInput.addEventListener('change', handlePaymentMethodChange);
        console.log('✅ Payment method input initialized');
    }

    const receiptForm = document.getElementById('receiptForm');
    if (receiptForm) {
        receiptForm.addEventListener('submit', validateReceiptForm);
        console.log('✅ Receipt form initialized');
    }

    // Set current user and date
    setDefaultValues();
    
    document.addEventListener('click', closeSuggestions);
    console.log('✅ Customer Receipt initialization complete');
}

function setDefaultValues() {
    // Set current user as collected by
    const currentUser = document.getElementById('currentUser')?.value || 'Current User';
    document.getElementById('collectedBy').value = currentUser;
    
    // Set current date as collection date
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('collectionDate').value = today;
    
    console.log('✅ Default values set - User:', currentUser, 'Date:', today);
}

function handleCustomerSearch() {
    const query = this.value.trim();
    console.log(`🔍 CUSTOMER RECEIPT: Searching customers for: "${query}"`);
    
    if (query.length < 2) {
        clearCustomerSuggestions();
        return;
    }
    
    fetch(`/ajserp/customer-receipt-suggestions/?q=${encodeURIComponent(query)}`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log(`✅ CUSTOMER RECEIPT: Found ${data.length} customer suggestions`, data);
            displayCustomerSuggestions(data);
        })
        .catch(error => {
            console.error('❌ CUSTOMER RECEIPT: Error fetching customer suggestions:', error);
            showError('Error loading customer suggestions');
        });
}

function displayCustomerSuggestions(customers) {
    const suggestions = document.getElementById('customerSuggestions');
    if (!suggestions) {
        console.log('❌ CUSTOMER RECEIPT: Customer suggestions container not found');
        return;
    }
    
    suggestions.innerHTML = '';
    
    if (!customers || customers.length === 0) {
        const noResult = document.createElement('div');
        noResult.textContent = 'No customers found';
        suggestions.appendChild(noResult);
        suggestions.style.display = 'block';
        return;
    }
    
    customers.forEach(customer => {
        const div = document.createElement('div');
        const outstandingAmount = customer.outstanding_amount || 0;
        const displayText = `${customer.customer_code} - ${customer.customer_name} (Outstanding: ₹${outstandingAmount.toFixed(2)})`;
        div.textContent = displayText;
        
        div.addEventListener('click', function() {
            console.log(`✅ CUSTOMER RECEIPT: Selected customer:`, customer);
            selectCustomer(customer);
        });
        
        suggestions.appendChild(div);
    });
    
    suggestions.style.display = 'block';
}

function clearCustomerSuggestions() {
    const suggestions = document.getElementById('customerSuggestions');
    if (suggestions) {
        suggestions.innerHTML = '';
        suggestions.style.display = 'none';
    }
}

function selectCustomer(customer) {
    console.log(`🎯 CUSTOMER RECEIPT: Selecting customer:`, customer);
    
    document.getElementById('customerCode').value = customer.customer_code;
    document.getElementById('customerName').value = customer.customer_name;
    
    const outstandingAmount = customer.outstanding_amount || 0;
    document.getElementById('totalOutstanding').value = outstandingAmount.toFixed(2);
    console.log(`💰 CUSTOMER RECEIPT: Auto-filled outstanding amount: ₹${outstandingAmount.toFixed(2)}`);
    
    document.getElementById('amountCollected').value = '';
    document.getElementById('balanceOutstanding').value = '';
    
    // Enable amount collected field
    document.getElementById('amountCollected').disabled = false;
    
    // Fetch customer invoices
    fetchCustomerInvoices(customer.customer_code);
    
    clearCustomerSuggestions();
    console.log('✅ CUSTOMER RECEIPT: Customer selection completed');
}

function fetchCustomerInvoices(customerCode) {
    console.log(`📋 CUSTOMER RECEIPT: Fetching invoices for customer: ${customerCode}`);
    
    fetch(`/ajserp/get-customer-invoices/?customer_code=${encodeURIComponent(customerCode)}`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log(`✅ CUSTOMER RECEIPT: Found ${data.invoices ? data.invoices.length : 0} invoices`, data);
            populateInvoiceDropdown(data.invoices);
        })
        .catch(error => {
            console.error('❌ CUSTOMER RECEIPT: Error fetching customer invoices:', error);
        });
}

function populateInvoiceDropdown(invoices) {
    const dropdown = document.getElementById('dropdown');
    if (!dropdown) {
        console.log('❌ CUSTOMER RECEIPT: Invoice dropdown not found');
        return;
    }
    
    dropdown.innerHTML = '';
    
    // Add Select All option
    const selectAllLabel = document.createElement('label');
    selectAllLabel.innerHTML = `
        <input type="checkbox" value="selectAll" id="selectAll" 
               onclick="toggleAllInvoices(this); event.stopPropagation();" style="margin-right: 8px">
        Select All
    `;
    dropdown.appendChild(selectAllLabel);
    
    // Add invoice options
    if (invoices && invoices.length > 0) {
        invoices.forEach(invoice => {
            const label = document.createElement('label');
            label.innerHTML = `
                <input type="checkbox" value="${invoice.document_number}" 
                       onclick="updateSelectedInvoices(); event.stopPropagation();" style="margin-right: 8px">
                ${invoice.document_number} - ₹${parseFloat(invoice.dr_amount || 0).toLocaleString('en-IN')} (${new Date(invoice.date).toLocaleDateString()})
            `;
            dropdown.appendChild(label);
        });
        console.log(`✅ CUSTOMER RECEIPT: Populated ${invoices.length} invoices in dropdown`);
    } else {
        const noInvoicesLabel = document.createElement('label');
        noInvoicesLabel.innerHTML = `<span style="margin-right: 8px">No unpaid invoices found</span>`;
        dropdown.appendChild(noInvoicesLabel);
        console.log('ℹ️ CUSTOMER RECEIPT: No unpaid invoices found for customer');
    }
}

function toggleAllInvoices(source) {
    const checkboxes = document.querySelectorAll('#dropdown input[type="checkbox"]:not(#selectAll)');
    checkboxes.forEach(checkbox => {
        checkbox.checked = source.checked;
    });
    updateSelectedInvoices();
    console.log(`📋 CUSTOMER RECEIPT: Toggled all invoices - ${source.checked ? 'selected' : 'deselected'} all`);
}

function updateSelectedInvoices() {
    const checkboxes = document.querySelectorAll('#dropdown input[type="checkbox"]:not(#selectAll)');
    const selectedValues = Array.from(checkboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.value);
    
    // Update hidden field for form submission
    document.getElementById('selectedInvoices').value = JSON.stringify(selectedValues);
    
    // Update dropdown button text
    const placeholder = document.getElementById('placeholder');
    if (selectedValues.length > 0) {
        placeholder.textContent = selectedValues.join(', ');
    } else {
        placeholder.textContent = 'Select Invoice Number';
    }
    
    console.log(`📋 CUSTOMER RECEIPT: Selected ${selectedValues.length} invoices:`, selectedValues);
}

// 🔧 CHANGED FUNCTION NAME: calculateBalanceFromLedger → calculateCustomerBalance
function calculateCustomerBalance() {
    const customerCode = document.getElementById('customerCode').value;
    const amountCollected = parseFloat(document.getElementById('amountCollected').value) || 0;
    const totalOutstanding = parseFloat(document.getElementById('totalOutstanding').value) || 0;
    
    console.log(`🧮 CUSTOMER RECEIPT: Calculating balance - Customer: ${customerCode}, Amount: ${amountCollected}, Outstanding: ${totalOutstanding}`);
    
    if (!customerCode) {
        console.log('⚠️ CUSTOMER RECEIPT: No customer selected');
        showError('Please select a customer first');
        document.getElementById('amountCollected').value = '';
        return;
    }
    
    if (amountCollected === 0) {
        updateCustomerBalanceDisplay(totalOutstanding); // ← CHANGED
        return;
    }
    
    if (amountCollected < 0) {
        showError('Amount collected cannot be negative');
        document.getElementById('amountCollected').value = '';
        return;
    }
    
    fetch(`/ajserp/get-customer-balance-after-receipt/?customer_code=${customerCode}&amount_collected=${amountCollected}`)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            console.log('📊 CUSTOMER RECEIPT: Balance calculation API response:', data);
            if (data.success) {
                updateCustomerBalanceDisplay(data.balance_after); // ← CHANGED
            } else {
                const localBalance = totalOutstanding - amountCollected;
                updateCustomerBalanceDisplay(localBalance); // ← CHANGED
            }
        })
        .catch(error => {
            console.error('❌ CUSTOMER RECEIPT: Error calculating balance:', error);
            const localBalance = totalOutstanding - amountCollected;
            updateCustomerBalanceDisplay(localBalance); // ← CHANGED
        });
}

// 🔧 CHANGED FUNCTION NAME: updateBalanceDisplay → updateCustomerBalanceDisplay
function updateCustomerBalanceDisplay(balance) {
    const balanceField = document.getElementById('balanceOutstanding');
    if (!balanceField) {
        console.log('❌ CUSTOMER RECEIPT: Balance field not found');
        return;
    }
    
    balanceField.value = balance.toFixed(2);
    
    if (balance < 0) {
        balanceField.style.border = '2px solid red';
        balanceField.style.color = 'red';
        balanceField.title = 'Amount collected exceeds outstanding amount - This will create an advance';
        console.log('⚠️ CUSTOMER RECEIPT: Amount collected exceeds outstanding amount');
    } else {
        balanceField.style.border = '';
        balanceField.style.color = '';
        balanceField.title = '';
    }
    
    console.log(`📊 CUSTOMER RECEIPT: Updated balance display: ₹${balance.toFixed(2)}`);
}

function handlePaymentMethodChange() {
    const paymentMethod = this.value;
    const paymentReferenceField = document.getElementById('paymentReference');
    
    console.log(`💳 CUSTOMER RECEIPT: Payment method changed to: ${paymentMethod}`);
    
    // Set placeholder based on payment method
    switch(paymentMethod) {
        case 'Cheque':
            paymentReferenceField.placeholder = 'Enter Cheque Number';
            break;
        case 'DD':
            paymentReferenceField.placeholder = 'Enter Demand Draft Number';
            break;
        case 'NEFT':
        case 'RTGS':
            paymentReferenceField.placeholder = 'Enter UTR Number';
            break;
        case 'UPI':
            paymentReferenceField.placeholder = 'Enter UPI Transaction ID';
            break;
        default:
            paymentReferenceField.placeholder = 'Payment Reference';
    }
    
    console.log(`💳 CUSTOMER RECEIPT: Payment reference placeholder set to: ${paymentReferenceField.placeholder}`);
}

function validateReceiptForm(e) {
    console.log('🔍 CUSTOMER RECEIPT: Starting form validation...');
    
    // DEBUG: Get ALL form values
    const formData = {
        customer_code: document.getElementById('customerCode').value,
        customer_name: document.getElementById('customerName').value,
        collected_by: document.getElementById('collectedBy').value,
        collection_date: document.getElementById('collectionDate').value,
        amount_collected: document.getElementById('amountCollected').value,
        total_outstanding: document.getElementById('totalOutstanding').value,
        balance_outstanding: document.getElementById('balanceOutstanding').value,
        payment_method: document.getElementById('paymentMethod').value,
        payment_reference: document.getElementById('paymentReference').value,
        invoice_numbers: document.getElementById('selectedInvoices').value,
        remarks: document.getElementById('remarks').value
    };
    
    console.log('📋 CUSTOMER RECEIPT: Form data:', formData);
    
    const customerCode = formData.customer_code;
    const amountCollected = parseFloat(formData.amount_collected) || 0;
    const totalOutstanding = parseFloat(formData.total_outstanding) || 0;
    const paymentMethod = formData.payment_method;
    
    console.log(`📋 CUSTOMER RECEIPT: Key fields - Customer: ${customerCode}, Amount: ${amountCollected}, Outstanding: ${totalOutstanding}, Method: ${paymentMethod}`);
    
    let isValid = true;
    let errorMessage = '';
    
    // Basic validation
    if (!customerCode) {
        errorMessage = 'Please select a customer';
        isValid = false;
    } else if (amountCollected <= 0) {
        errorMessage = 'Amount collected must be greater than 0';
        isValid = false;
    } else if (!paymentMethod || paymentMethod === 'Select type') {
        errorMessage = 'Please select payment method';
        isValid = false;
    }
    
    console.log('✅ Form validation result:', isValid, errorMessage);
    
    if (!isValid) {
        e.preventDefault();
        console.log('❌ CUSTOMER RECEIPT: Validation failed:', errorMessage);
        showError(errorMessage);
        return;
    }
    
    // Warn if amount collected exceeds outstanding
    if (amountCollected > totalOutstanding) {
        const confirmReceipt = confirm(
            `⚠️ Receipt Alert!\n\n` +
            `Amount collected: ₹${amountCollected.toFixed(2)}\n` +
            `Outstanding amount: ₹${totalOutstanding.toFixed(2)}\n\n` +
            `This receipt exceeds the outstanding amount and will create an advance.\n\n` +
            `Do you want to continue?`
        );
        
        if (!confirmReceipt) {
            e.preventDefault();
            console.log('❌ CUSTOMER RECEIPT: User cancelled receipt due to amount exceeding outstanding');
            return;
        }
    }
    
    console.log('✅ CUSTOMER RECEIPT: Form validation passed - SUBMITTING FORM');
    // Form will submit normally if we reach here
}

function toggleDropdown(event) {
    event.preventDefault();
    const dropdown = document.getElementById('dropdown');
    dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
    console.log('📋 CUSTOMER RECEIPT: Toggled invoice dropdown');
}

function closeSuggestions(e) {
    const suggestions = document.getElementById('customerSuggestions');
    const searchInput = document.getElementById('customerCode');
    
    if (suggestions && !e.target.matches('#customerCode')) {
        suggestions.innerHTML = '';
        suggestions.style.display = 'none';
    }
    
    // Close invoice dropdown when clicking outside
    const dropdown = document.getElementById('dropdown');
    const dropdownBtn = document.getElementById('dropdownBtn');
    if (dropdown && dropdownBtn && !dropdown.contains(e.target) && !dropdownBtn.contains(e.target)) {
        dropdown.style.display = 'none';
    }
}

function showError(message) {
    console.error('💥 CUSTOMER RECEIPT: Error:', message);
    alert('❌ ' + message);
}

console.log('🧾 Customer Receipt JavaScript ready');