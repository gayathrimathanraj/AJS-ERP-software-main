function addConditionField() {
  const container = document.getElementById('termsConditionsContainer');
  const index = container.querySelectorAll('.terms-condition-item').length + 1;

  const wrapper = document.createElement('div');
  wrapper.className = 'terms-condition-item mb-2';

  wrapper.innerHTML = `
    <label class="form-label">Condition ${index}</label>
    <textarea name="terms_conditions_list" class="form-control" rows="2" required></textarea>
  `;

  container.appendChild(wrapper);
}

