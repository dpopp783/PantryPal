
$(document).ready( () => {
    $("#view-popup").on("show.bs.modal", view);
    $("#use-recipe").on("click", use);
    $(".shop").on("click", buy_ingredients);
})

function view (event) {
    let id = Number($(event.relatedTarget).data("id"));
    if (id) {
        let recipe = recipes[id];

        $("#use-recipe").attr("data-id", recipe.id);
        $("#recipe-name").html(recipe.name);
        $("#recipe-image").attr("src", recipe.image);
        $("#recipe-link").attr("href", recipe.link)
    };
}

function use () {
    let id = Number($(this).data("id"));
    let recipe = recipes[id];
    $('#view-popup').modal('hide');
    fetch("/recipes/make-recipe", {
        method: "POST",
        body: JSON.stringify(recipe),
        headers: {
            "Content-type": "application/json"
        }
    });
    
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

