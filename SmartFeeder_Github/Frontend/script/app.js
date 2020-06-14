const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);


//#region *** DOM references
let html_waterHolder, html_voedingHolder, html_portieHolder, html_voedermomentenHolder, html_portiesHolder, html_meanHolder, html_totaalHolder, html_addHolder;
//#endregion

//#region *** Callback-Visualisation - show__
const showWater = function(jsonObject){
  //html elementen maken
  let waterhtml = ""
   for(const meting of jsonObject.water){
  waterhtml += `${meting.Waarde}`;
  }
  waterhtml += "%"
  //tonen
  html_waterHolder.innerHTML = waterhtml

};

const showVoeding = function(jsonObject){
  let stand ='';
  let waarde = 0;
  //html elementen maken
  let voedinghtml = ""
   for(const meting of jsonObject.voeding){
    waarde = `${meting.Waarde}`;
    stand += waarde.toString();
  }
  if(stand == 11){
    voedinghtml += ">75%"
  }
  else if(stand == 01){
    voedinghtml += "±50%"
  }
  else if(stand == 00){
    voedinghtml += "<25%"
  }
  //tonen
  html_voedingHolder.innerHTML = voedinghtml
};

const showPortie = function(jsonObject){
  //html elementen maken
  let portiehtml = "Laatste voedermoment: "
   for(const meting of jsonObject.portie){
  datum = `${meting.Datum}`;
  }
  portiehtml += datum.substring(4,datum.length - 7);
  //tonen
  html_portieHolder.innerHTML = portiehtml

};

const showVoedermomenten = function(jsonObject){
  //html elementen maken
  let voedermomentenhtml = `<tr>
                            <td>
                                Uur
                            </td>
                            <td class="c-table-h">
                                Gram
                            </td>
                            <td class="c-table-h">
                              <h5></h5>
                          </td>`;
   for(const voedermoment of jsonObject.voedermomenten){
    let Uur = voedermoment.Uur
    Uur = Uur.substring(0,Uur.length - 3); 
    voedermomentenhtml += `<tr>
                            <td>
                            ${Uur}
                            </td>
                            <td class="c-table-g">
                            ${voedermoment.Gewicht}g
                            </td>
                            <td class="c-table-delete">
                              <svg class="js-delete" data-voedermoment-id=${voedermoment.VoedermomentID} xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0z" fill="none"/><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg>
                            </td>
                          </tr>`;
  }

  //tonen
  html_voedermomentenHolder.innerHTML = voedermomentenhtml
  listenToClickRemoveVoedermoment();
};

const showPorties = function(jsonObject){
  let totaal = 0;
  let mean = 0;
  let aantal = 0;
  //html elementen maken
  let portieshtml = `<tr>
                      <td>
                          Datum
                      </td>
                      <td class="c-table-h">
                          Uur
                      </td>
                      <td>
                          Gram
                      </td>
                      </tr>`;

  let converted_labels = [];
  let converted_data = [];

   for(const meting of jsonObject.porties){
     let jsondatum = `${meting.Datum}`;
     let datum = jsondatum.substring(4,jsondatum.length - 12)
     let uur = jsondatum.substring(17,jsondatum.length - 7)
     let datumlang = `${datum.substring(0,datum.length - 5)} ${uur}`
     totaal += meting.Waarde
     aantal += 1
    portieshtml += `<tr>
                    <td class="c-table-content">
                        ${datum}
                    </td>
                    <td class="c-table-content">
                        ${uur}
                    </td>
                    <td class="c-table-content">
                        ${meting.Waarde}g
                    </td>
                    </tr>`;

    converted_labels.push(datumlang);
    converted_data.push(meting.Waarde);
  }
  mean = totaal/aantal


  //tonen
  html_portiesHolder.innerHTML = portieshtml

  let totaalhtml = `${totaal}g`
  html_totaalHolder.innerHTML = totaalhtml

  let meanhtml = `${mean}g`
  html_meanHolder.innerHTML = meanhtml

  drawChart(converted_labels, converted_data);
};


const drawChart = function(labels, data){
  let ctx = document.querySelector('.js-chart').getContext('2d');

  let config = {
      type: 'line', //Specifieert wat voor chart het is
      data: {
          labels: labels, //alle labels die aan de onderkant zullen getoond worden
          datasets: [
              {
                  label: 'Gewicht van portie', //label dat we aan de bovenkant zetten
                  backgroundColor: 'white',
                  borderColor: '#FD714F',
                  data: data, //data dat weergegeven moet worden
                  fill: false
              }
          ]
      },
      options: { //opties om de stijl en gedrag van de kaart aan te passen
          responsive: true,
          title: {
              display: false,
              text: ''
          },
          tooltip: {
              mode: 'index',
              intersect: true
          },
          hover: {
              mode: 'nearest',
              intersect: true
          },
          legend:{
            display: false
          },
          scales: {
              xAxes: [
                  {
                    ticks:{
                      fontSize: 14,
                      fontColor: '#293241',
                      fontFamily: 'Interstate',
                    },
                      display: true,
                      scaleLabel: {
                          display: false,
                          labelString: 'Datum en tijd'
                      }
                  }
              ],
              yAxes: [
                  {
                    ticks:{
                      fontSize: 20,
                      fontColor: '#293241',
                      fontFamily: 'Interstate',
                    },
                      display: true,
                      scaleLabel: {
                          display: false,
                          labelString: 'Gewicht'
                      }
                  }
              ]
          }
      }
  };
  let myChart = new Chart(ctx, config);
};

//#endregion

//#region *** Callback-No Visualisation - callback___
const callbackRemoveVoedermoment = function(data) {
  console.log(data);
  getVoedermomenten();
};

const callbackAddVoedermoment = function(data) {
  console.log("ADD antw van server ");
  if (data.treinid > 0) {
    console.log("ADD gelukt");
    console.log(data);

    //leegmaken
    document.querySelector("#add_uur").checked = "";
    document.querySelector("#add_gram").selectedIndex = "";
    window.alert("Het nieuwe voedermoment werd toegevoeg")
  }
};
//#endregion

//#region *** Data Access - get___
const getWater = function() {
  handleData('http://169.254.10.1:5000/water',showWater);
};

const getVoeding = function() {
  handleData('http://169.254.10.1:5000/voeding',showVoeding);
};

const getPortie = function() {
  handleData('http://169.254.10.1:5000/portie',showPortie);
};

const getPorties = function() {
  handleData('http://169.254.10.1:5000/porties',showPorties);
};

const getVoedermomenten = function() {
  handleData('http://169.254.10.1:5000/voedermomenten',showVoedermomenten);
};

//#endregion

//#region *** Event Listeners - ListenTo___
const listenToClickRemoveVoedermoment = function() {
  const buttons = document.querySelectorAll(".js-delete");
  for (const b of buttons) {
    b.addEventListener("click", function() {
      const id = b.getAttribute("data-voedermoment-id");
      console.log("verwijder " + id);
      if (confirm("Weet  je zeker dat je dit voedermoment wilt verwijderen?")){
            handleData(`http://169.254.10.1:5000/voedermoment/${id}`, callbackRemoveVoedermoment, null, "DELETE");
      }
    });
  }
};

const listenToClickAddVoedermoment = function() {
  const button = document.querySelector("#id_add_voedermoment");
  button.addEventListener("click", function() {
    console.log("toevoegen nieuw voedermoment");
    let gram = String(document.querySelector("#add_gram").value)
    let gramcheck = gram.includes("e")
    if (gramcheck == true){
      window.alert("U heeft en niet numerieke waarde ingegeven")
    }
    else{
      let uur = String(document.querySelector("#add_uur").value)
      uur += ":00"
      const jsonobject = {
        FeederCode: "0000000000",
        Uur: uur,
        Gewicht: document.querySelector("#add_gram").value
      };
      console.log(jsonobject);
      handleData("http://169.254.10.1:5000/voedermomenten", callbackAddVoedermoment, null, "POST", JSON.stringify(jsonobject));
    }
    
  });
};
//#endregion

//#region *** INIT / DOMContentLoaded
function loopHome(){
  getWater();
  getVoeding();
  getPortie();
  setTimeout(loopHome,900000)
}

const init = function() {
  html_waterHolder = document.querySelector(".js-water");
  html_voedingHolder = document.querySelector(".js-voeding");
  html_portieHolder = document.querySelector(".js-portie");

  html_voedermomentenHolder = document.querySelector(".js-voedermomenten")
  html_totaalHolder = document.querySelector(".js-totaal")
  html_meanHolder = document.querySelector(".js-mean")

  html_portiesHolder = document.querySelector(".js-porties")

  html_addHolder = document.querySelector(".js-add")

  console.info("DOM geladen...");
  
  if (html_waterHolder){
    loopHome();
  }
  if (html_voedermomentenHolder){
    // loopPlanning();
    getVoedermomenten();
  }
  if(html_portiesHolder){
    getPorties();
  }
  if(html_addHolder){
    console.log("js-add aanwezig")
    listenToClickAddVoedermoment(); 
  }
  
};

document.addEventListener("DOMContentLoaded", init);
//#endregion