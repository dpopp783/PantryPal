
$(document).ready( () => {
    $("#filter").on(); // TODO: Update
    $("#search").on("input", search);

    $("#modify-popup").on("show.bs.modal", modify);

    $("#save").on("click", submit);
    $("#remove").on("click", submit);
});

function search(){
    let key = $("#search").val().toLowerCase()

    $(".item.row").each((i, element) => {
        let row = $(element)
        if (row.attr("name").toLowerCase().includes(key)){
            row.css("display", "flex");
        } else {
            row.css("display", "none");
        }
    });
}

function filter(){
    // TODO: Add filter functionality
}

function modify(event){
    $("#modify-form")[0].reset()
    
    let id = Number($(event.relatedTarget).data("id"));

    if (id) {
        let item = inventory[id];
        $("#id").val(id);
        $("#name").val(item.ingredient.name);
        $("#quantity").val(item.quantity);
        $("#unit").val(item.unit);
        $("#expiration_date").val(item.expiration_date);
    }
}

function submit(){
    let form = $("#modify-form");
    let button = $(this);

    if (button.attr("id") == "save") {
        let id = Number($("#id"));
        if (inventory[id]){ // TODO: Make this display name but use ID
            form.attr("action", "/ingredients/modify")  
        } else {
            form.attr("action", "/ingredients/add")  
        }
    } else {
        form.attr("action", "/ingredients/remove")  
    }

    form.submit();
}
