
$(document).ready( () => {
    $("#view-popup").on("show.bs.modal", view);
    $(".shop").on("click", buy_ingredients);
})

function view (event) {
    let id = Number($(event.relatedTarget).data("id"));
    console.log(id)
    if (id) {
        let recipe = recipes[id];
        console.log(recipe)

        $("#recipe-name").html(recipe.name);
        $("#recipe-image").attr("src", recipe.image)
    }
}

function buy_ingredients () {
    console.log("TEST")
    let id = Number(this.id);
    let recipe = recipes[id];
    fetch("/recipes/buy-ingredients", {
        method: "POST",
        body: JSON.stringify(recipe),
        headers: {
            "Content-type": "application/json"
        }
    });
}

