
$(document).ready( () => {});

var inventory_updates = {};

function search(){
    let key = $("#search").val().toLowerCase()

    $(".item.row").each((i, element) => {
        if (inventory[element.id] && inventory[element.id].ingredient.name.toLowerCase().includes(key)){
            $("#"+element.id).css("display", "flex");
        } else {
            $("#"+element.id).css("display", "none");
        }
    });
}

function add(){
    // TODO: Add pop-up modification window

    
    let item = {}

    let table = $("#inventory");
    table.append(
        `<div class="item row py-1 pe-1 border-top border-dark-subtle bg-opacity-25 bg-success" id="`+ item.ingredient.id + `" style="align-items: center;">
            <div class="col-4">`+ item.ingredient.name + `</div>
            <div class="col-4">`+ item.quantity + ` ` + item.unit + `</div>
            <div class="col-3">`+ item.expiration_date + `</div>
            <div class="col-1">
                <div class="btn-group">
                    <button class="btn btn-warning border-0" title="Modify Ingredient" name="modify">
                        <i class="bi bi-pencil-square"></i>
                    </button>
                    <button class="btn btn-danger border-0" title="Remove Ingredient" name="remove">
                        <i class="bi bi-trash3-fill"></i>
                    </button>
                </div>
            </div>
        </div>`
    );

    table.find("[name='modify']").on("click", modify);
    table.find("[name='remove']").on("click", remove);
}

function reset(){
    let table = $("#inventory");
    table.children().remove();

    for (let id in inventory) {
        table.append(
            `<div class="item row py-1 pe-1 border-top border-dark-subtle bg-opacity-25" id="`+ inventory[id].ingredient.id + `" style="align-items: center;">
                <div class="col-4">`+ inventory[id].ingredient.name + `</div>
                <div class="col-4">`+ inventory[id].quantity + ` ` + inventory[id].unit + `</div>
                <div class="col-3">`+ inventory[id].expiration_date + `</div>
                <div class="col-1">
                    <div class="btn-group">
                        <button class="btn btn-warning border-0" title="Modify Ingredient" name="modify">
                            <i class="bi bi-pencil-square"></i>
                        </button>
                        <button class="btn btn-danger border-0" title="Remove Ingredient" name="remove">
                            <i class="bi bi-trash3-fill"></i>
                        </button>
                    </div>
                </div>
            </div>`
        );
    }

    table.find("[name='modify']").on("click", modify);
    table.find("[name='remove']").on("click", remove);

    inventory_updates = {}
    $("#filter").val(""); // TODO: Update
    $("#search").val("");

    // TODO: Toastr reset notification
}

function save(){
    // TODO: Add code to post request to back-end
}

function modify(){
    let row = $(this).closest(".item.row")
    let id = Number(row.attr("id"));
    
    // TODO: Add pop-up modification window

    let item = inventory[id];
    let item_updates = {
        ingredient: {
            name: row.children().eq(0).text(),
            id: id
        },
        quantity: Number(row.children().eq(1).text().split(" ")[0]),
        unit: row.children().eq(1).text().split(" ")[1],
        expiration_date: row.children().eq(2).text()
    };

    if (row.hasClass("bg-success")) {
        inventory_updates[id] = item_updates;
    } else if (
        item.ingredient.id != item_updates.ingredient.id ||
        item.quantity != item_updates.quantity ||
        item.unit != item_updates.unit ||
        item.expiration_date != item_updates.expiration_date
    ) {
        inventory_updates[id] = item_updates;
        row.addClass("bg-warning");
    } else {
        delete inventory_updates[id];
        row.removeClass("bg-warning");
    }

}

function remove(){
    let row = $(this).closest(".item.row");
    let id = Number(row.attr("id"));

    if (row.hasClass("bg-success")) {
        delete inventory_updates[id];
        row.remove();
        return;
    } else if (row.hasClass("bg-danger")) {
        delete inventory_updates[id];
        row.removeClass("bg-danger");
        row.find("[name='modify']").prop("disabled", false);
    } else {
        inventory_updates[id] = {};
        row.addClass("bg-danger");
        row.find("[name='modify']").prop("disabled", true);
    }
}


$("#filter").on(); // TODO: Update
$("#search").on("input", search);
$("#add").on("click", add);
$("#reset").on("click", reset);
$("#save").on("click", save);
$("[name='modify']").on("click", modify);
$("[name='remove']").on("click", remove);
