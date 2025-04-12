console.log("Hello there!");


function initialize() {
    console.log("initializing");

    heart_beat().then(() => { console.log("finished")});

    allusers().then(() => { console.log("finished")});
}

// window.onload = initialize;

async function heart_beat() {
    console.log("Heart beat called");

    var res = await fetch("/heartbeat");
    res = await res.text();

    var beep = document.getElementById("beat");

    console.log(res);

    

    console.log("heartbeat called")

    beep.innerHTML = `<p>${res}</p>`;

}

async function allusers() {

    var beep = document.getElementById("allusers");
    var res = await fetch("/api/allusers");
    res = await res.text();

    beep.innerHTML = `<p>${res}</p>`;

}