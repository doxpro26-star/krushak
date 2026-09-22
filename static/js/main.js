function toggleLang(){
  const btn=document.getElementById('langBtn');
  if(btn.innerText.includes('मराठी')){btn.innerHTML='<i class="bi bi-translate me-1"></i>English'; alert('मराठी भाषांतर लवकरच — Marathi translation coming soon. Helpline: 1800-180-1551');}
  else{btn.innerHTML='<i class="bi bi-translate me-1"></i>मराठी';}
}
// bootstrap validation
(() => {
  const forms=document.querySelectorAll('.needs-validation');
  Array.from(forms).forEach(form=>{
    form.addEventListener('submit',e=>{
      if(!form.checkValidity()){e.preventDefault();e.stopPropagation();}
      form.classList.add('was-validated');
    });
  });
})();
