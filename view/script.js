const container = document.querySelector("#container");
const albumArt = document.querySelector("#art");
const trackTitle = document.querySelector("#title");
const trackArtist = document.querySelector("#artist");
const trackAlbum = document.querySelector("#album");
const audio = document.querySelector("#audio");
const loader = document.querySelector("#loader");
const bg = document.querySelector(".bg");

// when audio is played/stopped, give/remove the scaleUp class to the album art
audio.onplay = () => albumArt.classList.add("scaleUp");
audio.onpause = () => albumArt.classList.remove("scaleUp");

// get path, title, artist, album, and album art from query params
const params = new URLSearchParams(window.location.search);
const path = decodeURIComponent(params.get("path"));
const title = decodeURIComponent(params.get("title"));
const artist = decodeURIComponent(params.get("artist"));
const album = decodeURIComponent(params.get("album"));
const art = decodeURIComponent(params.get("art"));

// set the title, artist, album, and album art
// text stuff needs innerhtml not textcontent
trackTitle.innerHTML = title;
document.title = title;
trackArtist.innerHTML = artist;
trackAlbum.innerHTML = album;
albumArt.src = art;
bg.style.backgroundImage = `url('${art}')`;
audio.src = path;
// create favicon and set it to the album art
const favicon = document.createElement("link");
favicon.rel = "icon";
favicon.href = art;
document.head.appendChild(favicon);
// add hidden to loader and remove hidden from container
loader.classList.add("hidden");
container.classList.remove("hidden");
