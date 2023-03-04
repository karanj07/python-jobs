jQuery(".accordion-item button a.q-link").on("click", function(event){
    event.preventDefault();
    window.location.href = jQuery(this).attr("href")
});