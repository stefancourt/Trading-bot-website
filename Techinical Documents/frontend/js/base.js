const body = document.querySelector("body"),
      menuBtn = document.querySelector(".menu-button"),
      sidebar= document.querySelector(".sidebar"),
      backBtn = document.querySelector(".back"),
      darkBtn = document.querySelector(".mode-button");

      menuBtn.addEventListener("click", () =>{
          sidebar.classList.add("open");
          sidebar.classList.remove("close");
      })
      backBtn.addEventListener("click", () =>{
          sidebar.classList.remove("open");
          sidebar.classList.add("close");
      })
      darkBtn.addEventListener("click", () =>{
          if (body.classList.contains("light")) {
            body.classList.remove("light")
            body.classList.add("dark");
          }
          else if (body.classList.contains("dark")) {
            body.classList.remove("dark");
            body.classList.add("light");
          }
      })