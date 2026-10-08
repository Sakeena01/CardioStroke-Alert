document.querySelectorAll(".sidebar a").forEach(item=>{

item.addEventListener("mouseenter",()=>{

item.style.boxShadow="0 0 25px #00E5FF";

});

item.addEventListener("mouseleave",()=>{

item.style.boxShadow="none";

});

});