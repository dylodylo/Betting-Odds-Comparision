 function myFunction() {
           var input, filter, table, tr, td,td2, i, txtValue,txtValue;
           input = document.getElementById("myInput");
           filter = input.value.toUpperCase();
           table = document.getElementById("myTable");
           tr = table.getElementsByTagName("tr");
           for (i = 0; i < tr.length; i++) {
             td = tr[i].getElementsByTagName("td")[0];
	     td2 = tr[i].getElementsByTagName("td")[1];
             if (td || td2) {
               txtValue = td.textContent || td.innerText;
	       txtValue2 = td2.textContent || td2.innerText;
               if (txtValue.toUpperCase().indexOf(filter) > -1 || txtValue2.toUpperCase().indexOf(filter) > -1 ) {
                 tr[i].style.display = "";
               } else {
                 tr[i].style.display = "none";
               }
             }       
           }
         }