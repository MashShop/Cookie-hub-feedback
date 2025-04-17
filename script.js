// language switcher
const langSelect = document.getElementById('lang');
function applyLang(lang) {
  document.querySelectorAll('[data-en]').forEach(el => {
    el.textContent = el.dataset[lang];
  });
}
langSelect.addEventListener('change', () => applyLang(langSelect.value));
// initialize
applyLang('en');

// form submission with 3‑send & 10‑min cooldown enforced server‑side
document.getElementById('feedbackForm').addEventListener('submit', async e => {
  e.preventDefault();
  const msg = document.getElementById('feedbackMessage').value.trim();
  if (!msg) return alert('Please write your feedback.');

  try {
    const res = await fetch('/send-feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg })
    });
    const data = await res.json();
    if (data.success) {
      alert(data.remaining
        ? `Feedback sent! You have ${data.remaining} tries left.`
        : 'Feedback sent! You’ve used all your chances.'
      );
      document.getElementById('feedbackMessage').value = '';
    } else {
      alert(data.error);
    }
  } catch (err) {
    console.error(err);
    alert('Error sending feedback.');
  }
});
