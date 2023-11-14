
$(document).ready( () => {
    $("#filter").on(); // TODO: Update
    $("#search").on("input", search);

    $("#modify-popup").on("show.bs.modal", modify);
    $("#purchase-popup").on("show.bs.modal", get_expiration);

    $("#save").on("click", submit);
    $("#remove").on("click", submit);
    $("#purchase").on("click", purchase);
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
        let item = shoppinglist[id];
        $("#id").val(id);
        $("#name").val(item.ingredient.name);
        $("#quantity").val(item.quantity);
        $("#unit").val(item.unit);
    }
}

function submit(){
    let form = $("#modify-form");
    let button = $(this);

    if (button.attr("id") == "save") {
        let id = Number($("#id").val());
        if (shoppinglist[id]){
            form.attr("action", "/shoppinglist/modify")
        } else {
            form.attr("action", "/shoppinglist/add")
        }
    } else {
        form.attr("action", "/shoppinglist/remove")
    }
    form.submit();
}

function get_expiration(event){
    $("#p-expiration_date").val("")

    let id = Number($(event.relatedTarget).data("id"));
    let item = shoppinglist[id];

    $("#id").val(id);
    $("#name").val(item.ingredient.name);
    $("#quantity").val(item.quantity);
    $("#unit").val(item.unit);
}

function purchase(){ 
    let form = $("#modify-form");

    let id = $("#id").val();
    let expiration_date = $("#p-expiration_date").val();
    $("#expiration_date").val(expiration_date);
    
    form.attr("action", "/shoppinglist/purchase")
    form.submit();
}