
$(document).ready( () => {
    $("#view-popup").on("show.bs.modal", view);
})

function view (event) {
    let id = Number($(event.relatedTarget).data("id"));
    console.log(id)
    if (id) {
        let recipe = recipes[id];

        $("#recipe-name").attr("text", recipe.name);
        $("#recipe-image").attr("src", recipe.image)



    }


}

