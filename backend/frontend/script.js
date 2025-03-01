function convertText() {
    const fromLang = document.getElementById("fromLanguage").value;
    const toLang = document.getElementById("toLanguage").value;

    document.getElementById("output").innerHTML = `Converting from <b>${fromLang}</b> to <b>${toLang}</b>...`;
}
