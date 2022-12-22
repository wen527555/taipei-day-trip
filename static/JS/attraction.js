// get url id //
let url = location.href;
let id = url.split("attraction/")[1];

window.onload = function () {
  attraction(id);
};

function attraction(id) {
  fetch(`/api/attraction/${id}`)
    .then((response) => {
      return response.json();
    })
    .then((result) => {
      get_attraction(result);
      get_images(result);
    });
}

function get_attraction(result) {
  let name = result.data.name;
  const attrs_name = document.querySelector(".attrs_name");
  attrs_name.textContent = name;

  let category = result.data.category;
  let mrt = result.data.mrt;
  const attrs_name_info = document.querySelector(".attrs_name_info");
  attrs_name_info.textContent = category + " at " + mrt;

  let description = result.data.description;
  const attrs_description = document.querySelector(".attrs_description");
  attrs_description.textContent = description;

  let address = result.data.address;
  const attrs_address = document.querySelector(".address");
  attrs_address.textContent = address;

  let transport = result.data.transport;
  const attrs_transport = document.querySelector(".transport");
  attrs_transport.textContent = transport;
}

function get_images(result) {
  let attrs_images = document.querySelector("#image");
  for (let i = 0; i < result.data.images.length; i++) {
    let slides = document.createElement("div");
    slides.className = "slides fade";

    let image = result.data.images[i];
    let imgElement = document.createElement("img");
    imgElement.setAttribute("src", image);
    slides.appendChild(imgElement);

    attrs_images.appendChild(slides);
  }

  let flow_dot = document.querySelector(".flow_dot");
  for (let i = 0; i < result.data.images.length; i++) {
    const dots = document.createElement("p");
    dots.classList.add("dots");
    flow_dot.appendChild(dots);
  }

  showImage((slideIndex = 1));
}

let slideIndex = 0;
function showImage(n) {
  // for Display the first Image
  let slide = document.getElementsByClassName("slides");
  let dots = document.getElementsByClassName("dots");
  let i;
  // to prevent larger values than the slide length
  if (n > slide.length) {
    slideIndex = 1;
  }
  if (n < 1) {
    slideIndex = slide.length;
  }
  // make other images dispaly: none
  for (i = 0; i < slide.length; i++) {
    slide[i].style.display = "none";
  }
  slide[slideIndex - 1].style.display = "block";
  // to remove the active class from other dots
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  dots[slideIndex - 1].className += " active";
}

// for Next & Prev Actions
function plusIndex(n) {
  showImage((slideIndex += n));
}

// choose display image
function currentSlide(n) {
  showImage((slideIndex = n));
}

//select booking date --set after today
let today = new Date().toISOString().split("T")[0];
document.querySelector("#choose_date").setAttribute("min", today);

// select booking time & price //
if (document.querySelector('input[name="time"]')) {
  document.querySelectorAll('input[name="time"]').forEach((elem) => {
    elem.addEventListener("change", function (event) {
      let item = event.target.value;
      if (item == "afternoon") {
        choose_time = "afternoon";
        document.querySelector(".price").innerHTML = "新台幣 2500 元";
      } else {
        choose_time = "morning";
        document.querySelector(".price").innerHTML = "新台幣 2000 元";
      }
    });
  });
}
