const ativos = ['ABEV3','B3SA3','BBAS3','BBDC4','BOVA11','ITSA4','ITUB4','MGLU3','PETR4','VALE3','VIIA3']

const vencimentos = [
    {
        data: '17/02/2023',
        du: 24,
        serieCall: 'B',
        seriePut: 'N'
    },
    {
        data: '17/03/2023',
        du: 42,
        serieCall: 'C',
        seriePut: 'O'
    },
    {
        data: '20/04/2023',
        du: 65,
        serieCall: 'D',
        seriePut: 'P'
    },
    {
        data: '19/05/2023',
        du: 84,
        serieCall: 'E',
        seriePut: 'Q'
    }
];

var select1 = document.getElementById("selectAtivo");
var select2 = document.getElementById("selectVencto");

function PreencheDropdown() {

    for(var i = 0; i < ativos.length; i++) {

        var opt1 = ativos[i];
        var li = document.createElement("li");
        texto = `<input type='checkbox' id='check-${i.toString()}' name='check-${i.toString()}' value='${opt1}' onclick='AjustaLista()'><label for='check-${i.toString()}'>${opt1}</label>`
        li.setAttribute("id",`list-item-${i.toString()}`);
        li.setAttribute("class","list-item");
        select1.appendChild(li);
        document.getElementById(`list-item-${i.toString()}`).innerHTML = texto;
  
      };

    for(var i = 0; i < vencimentos.length; i++) {

      var opt2 = vencimentos[i]['data'] + " - " + vencimentos[i]['du'].toString() + " dias úteis";
      var el = document.createElement("option");
      el.textContent = opt2;
      el.value = opt2;
      select2.appendChild(el);

    };

};

//PreencheDropdown();

document.getElementById('selectVencto').onchange = function() {
    var vencto = this.value.substring(0,10);
    var i = vencimentos.findIndex(item => item.data == vencto)
    document.getElementById('serieC').value = vencimentos[i]['serieCall'];
    document.getElementById('serieP').value = vencimentos[i]['seriePut'];

}

//========================================================

function AjustaLista() {
    var j = 0;
    for(var i = 0; i < ativos.length; i++) {
        var checkBox = document.getElementById(`check-${i.toString()}`);
        if (j <= 7) {
            if (checkBox.checked == true) {
                document.getElementById(`papel-${j.toString()}`).value = checkBox.value;
                j++;
            } else {
                document.getElementById(`papel-${j.toString()}`).value = '';
            }
        }
    }
}

var papeis = []
const selectBtn = document.querySelector(".select-btn")
const items = document.querySelectorAll(".item");

selectBtn.addEventListener("click", () => {
    selectBtn.classList.toggle("open");
});

items.forEach(item => {
    item.addEventListener("click", () => {
        item.classList.toggle("checked");

        papeis = []

        let checked = document.querySelectorAll(".checked")
        let btnText = document.querySelector(".btn-text");

            // if(checked && checked.length > 0){
            //     btnText.innerText = `${checked.length} Selected`;
            // } else {
            //     btnText.innerText = "Select Ticker";
            // }

            checked.forEach(papel => {
                papeis.push(papel.id)
            })

        });

})