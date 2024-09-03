
myFunc(site);

function myFunc(variavel) {
    myArray = JSON.parse(variavel);
    const list = document.getElementById("tabela");
    for (i in myArray) {
        console.log(myArray[i]);
        // console.log(myArray[i]['sigma']);
        console.log(myArray[i][0]);
        console.log(myArray[i][1]);
        var tr = document.createElement('tr');
        tr.appendChild(document.createElement('td')).innerHTML = myArray[i][0];
        tr.appendChild(document.createElement('td')).innerHTML = myArray[i][1].toFixed(2);
        list.appendChild(tr);
    }
}
