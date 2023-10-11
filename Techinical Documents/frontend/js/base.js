const body = document.querySelector("body"),
      menuBtn = document.querySelector(".menu-button"),
      sidebar= document.querySelector(".sidebar"),
      backBtn = document.querySelector(".back");

      menuBtn.addEventListener("click", () =>{
          sidebar.classList.add("open");
          sidebar.classsList.remove("close");
      })
      backBtn.addEventListener("click", () =>{
          sidebar.classList.remove("open");
          sidebar.classList.add("close");
      })