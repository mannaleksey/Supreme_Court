var rows = document.getElementById("table_2").getElementsByTagName('tr'),
    rowsB = rows.length;

var col_th = rows[0].getElementsByTagName('th');
col_th[0].innerHTML = 'Дата';
col_th[1].innerHTML = 'Тип';
col_th[2].innerHTML = 'Результат';
for (var i=0; i<rowsB; i++)  //проходим строки таблицы
    {
        var row=rows[i]; //берём очередную строку
        row.deleteCell(-1); //удаляем последнюю ячейку
    }
