function stripWhitespace() {
    let input = document.querySelector("textarea");
    if(!input.value.replace(/\s/g, "")) {
        input.value = "";
    }
}
