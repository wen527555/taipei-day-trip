//串接旅遊景點 API ( /api/attractions )
let nextPage;
let isloading = false;
let keyword_value;

//先載入首頁
get_attractions("0");
// 設定觀察對象：告訴 observer 要觀察哪個目標元素
const footer = document.querySelector("footer");
// 響鈴條件：設定和控制在哪些情況下，呼叫 callback 函式
const options = {
  root: null,
  rootMargin: "0px",
  threshold: 0.5,
};
//製作鈴鐺：建立一個 intersection observer，帶入相關設定資訊
const observer = new IntersectionObserver(callback, options);

//設定觀察對象：告訴鈴鐺要觀察哪個目標元素
observer.observe(footer);

//載入attractions資訊的函式
function get_attractions(page) {
  let url = `/api/attractions?page=${page}`;
  attractionsFetch(url);
}

function attractionsFetch(url) {
  isloading = true;
  fetch(url)
    .then((response) => {
      return response.json();
    })
    .then((result) => {
      appendContent(result);
      nextPage = result.nextPage;
    });
}

let search_keyword = document.querySelector(".search_button");
search_keyword.addEventListener("click", () => {
  keyword_value = document.getElementById("keyword_value").value;
  let url = `/api/attractions?page=0&keyword=${keyword_value}`;
  document.querySelector("main").innerHTML = "";
  keywordFetch(url);
});

function keywordFetch(url) {
  isloading = true;
  fetch(url)
    .then((response) => {
      return response.json();
    })
    .then((result) => {
      if (result.error == true) {
        document.querySelector("main").innerHTML = "查無此搜尋結果";
      }
      appendContent(result);
      nextPage = result.nextPage;
    });
}

function getcatgory() {
  isloading = true;
  fetch(`/api/categories`)
    .then((response) => {
      return response.json();
    })
    .then((result) => {
      let catgories = document.getElementsByClassName("Welcome_search");
      let categoryview = document.createElement("div");
      categoryview.classList.add("categoryview");
      for (i = 0; i < result.data.length; i++) {
        let category = result.data[i];
        let item_button = document.createElement("button");
        item_button.classList.add("categoryitem");

        let item_text = document.createElement("text");
        item_text.classList.add("categoryitem_text");
        index = "categoryitem_text" + i;
        item_text.setAttribute("id", index);
        let item_button_text = document.createTextNode(category);

        item_text.appendChild(item_button_text);
        item_button.appendChild(item_text);

        categoryview.appendChild(item_button);
      }
      catgories[0].appendChild(categoryview);
    });
  isloading = false;
}
getcatgory();

function categoryview() {
  const category_list1 = document.querySelector(".category_list");
  category_list1.style.display = "flex";

  const categoryview = document.querySelector(".categoryview");
  categoryview.style.display = "flex";

  //偵測分類按鈕點擊

  for (i = 0; i < 9; i++) {
    const viewtext = document.getElementById("categoryitem_text" + i);
    viewtext.addEventListener("click", function (e) {
      // console.log(e.target.textContent);

      inputbox = document.getElementsByClassName("categoryitem");
      inputbox = e.target.textContent;
      // console.log(inputbox);

      let inputtext = document.getElementById("keyword_value");
      inputtext.setAttribute("value", inputbox);

      const viewblock = document.querySelector(".categoryview");
      viewblock.style.display = "none";
    });
  }
}

function hideview() {
  const view = document.querySelector(".categoryview");
  view.style.display = "none";
  const category_list2 = document.querySelector(".category_list");
  category_list2.style.display = "none";
}

isloading = true;
function appendContent(result) {
  for (let i = 0; i < result.data.length; i++) {
    let image = result.data[i].images[0];
    let name = result.data[i].name;
    let mrt = result.data[i].mrt;
    let category = result.data[i].category;
    const main = document.querySelector("main");
    main.classList.add("main");
    const all_items = document.createElement("a");
    all_items.classList.add("attr");
    main.prepend(all_items);

    const attr_img = document.createElement("img");
    attr_img.src = image;
    attr_img.classList.add("attr_img");
    all_items.appendChild(attr_img);

    const attr_name = document.createElement("div");
    attr_name.classList.add("attr_name");
    attr_name.textContent = name;
    all_items.appendChild(attr_name);

    const attr_box = document.createElement("div");
    attr_box.classList.add("attr_box");

    const attr_mrt = document.createElement("div");
    attr_mrt.classList.add("attr_mrt");
    attr_mrt.textContent = mrt;
    attr_box.appendChild(attr_mrt);

    const attr_cat = document.createElement("div");
    attr_cat.classList.add("attr_cat");
    attr_cat.textContent = category;
    attr_box.appendChild(attr_cat);

    all_items.appendChild(attr_box);
    main.appendChild(all_items);
  }
  nextPage = result.data.nextPage;
  isloading = false;
}

//條件達成做什麼：符合設定條件下，目標進入或離開viewpoet時觸發此callback函式
function callback() {
  if (nextPage == "null") {
    return;
  }
  if (keyword_value && isloading == false) {
    let url = `/api/attractions?page=${nextPage}&keyword=${keyword_value}`;
    keywordFetch(url);
  } else if (nextPage && isloading == false) {
    let url = `/api/attractions?page=${nextPage}`;
    attractionsFetch(url);
  }
}

// window.onload = function () {
//   let keyword_value = document.getElementById("keyword_value").value;
//   keyword_value.onfocus = function () {
//     if ((keyword_value = "")) {
//       window.location.reload();
//     }
//   };
// };
