function toogleNavBar() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav inner") {
        x.className += " responsive";
    } else {
        x.className = "topnav inner";
    }
}

function confirmation() {
    return confirm('Are you sure?');
}

function filterTable(n) {
    // Declare variables 
    var input, filter, table, tr, td, i, odd;
    input = document.getElementById("searchTableBox");
    filter = input.value.toUpperCase();
    table = document.getElementById("dataTable");
    tr = table.getElementsByTagName("tr");
    odd = true
  
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 1; i < tr.length - 1; i++) {
        td = tr[i].getElementsByTagName("td")[n];
        if (td) {
            if (td.getElementsByTagName("a")[0].innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }

    // Apply alternating bg-colors to rows
    for (i = 1; i < tr.length - 1; i++) {
        if (tr[i].style.display === "none") {
            continue;
        } else {
            if (odd) {
                tr[i].style.backgroundColor = "transparent"
            } else {
                tr[i].style.backgroundColor = "#D2E7EF"
            }
            odd = !odd
        }
    }
}
