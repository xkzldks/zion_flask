var slideIndex = 1;
        showDivs(slideIndex);

        function plusDivs(n) {
          showDivs(slideIndex += n);
        }

        function currentDiv(n) {
          showDivs(slideIndex = n);
        }

        function showDivs(n) {
          var i;
          var x = document.getElementsByClassName("mySlides");
          var dots = document.getElementsByClassName("demo");
          var img1 = document.getElementsByClassName("img1");
          if (n > x.length) {slideIndex = 1}
          if (n < 1) {slideIndex = x.length} ;
          for (i = 0; i < x.length; i++) {
             x[i].style.transition = "1s ease-out";
             x[i].style.display = "none";
             x[i].style.border = "outset";
          }
          for (i = 0; i < dots.length; i++) {
             dots[i].className = dots[i].className.replace(" w3-border-red", "");
          }
          for (i = 0; i < img1.length; i++) {
            if(i == n-1){
             img1[i].style.opacity = "100%";
<!--                 img1[i].style.border = "outset";-->
             }
             else if(i != n-1){
                img1[i].style.opacity = "70%";
                img1[i].style.transition = "1s ease-out";
                img1[i].style.border = "none";
             }
          }
          x[slideIndex-1].style.display = "block";
          dots[slideIndex-1].className += " w3-border-red";
        }

        $("#touchSlider").touchSlider({
            // ... Options
            page: 2
        });