var table = document.getElementById('table_1'),
    tr = table.getElementsByTagName('tr'),
    rows = tr.length, tmp;
var col_th = tr[0].getElementsByTagName('th');
tmp = col_th[2].innerHTML;
col_th[2].innerHTML = col_th[0].innerHTML;
col_th[0].innerHTML = tmp;
col_th[0].innerHTML = 'Дата';
col_th[1].innerHTML = 'Состояние';
col_th[2].innerHTML = 'Документ-основание';
for (var i=1; i<rows; i++)
    { var col = tr[i].getElementsByTagName('td');

      tmp = col[2].innerHTML;
      col[2].innerHTML = col[0].innerHTML;
      col[0].innerHTML = tmp;
    }