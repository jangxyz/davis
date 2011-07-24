function parseData(index, container) {
    //
    var dataTable = $('table#data-' + (index+1) + '-table' , container);
    var data = $('tr', dataTable).map(function(index, tr) {
        var x = $("td input.x-coord-value", tr).val();
        var y = $("td input.y-coord-value", tr).val();
        return [[ parseFloat(x),parseFloat(y) ]];
    });

    return data;
}

function parseLabel(index, container) {
    var graphContainer = $('#graph-' + (index+1));
    var isChecked = $('input:checkbox.show-label', graphContainer)[0].checked;
    if (!isChecked) {
        return ;
    }
    var label = $('input#label-' + (index+1), graphContainer);
    return label.attr('value');
}

function parseType(index, container) {
    var selected = $('select[name=graph-' + (index+1) + '-type]', container).select();
    return selected.val();
}

function readDataOptions(index, data_array) {
    // data
    var result = {
        data: data_array
    };

    // label
    var label = parseLabel(index);
    if (label) {
        result['label'] = label;
    };

    // graph type
    var graphType = parseType(index);
    // bars
    if (graphType == 'bars') {
        result['bars'] = {show: true};
    } 
    // lines + points
    else {
        result['lines'] = {show: true};
        result['points'] = {show: true};
    }

    return result;
}

function redraw() {
    var dataObjectSet = $('.graph-container').map(function(index, graphContainer) {
        // read data
        var dataSeries = parseData(index, graphContainer);
        
        // options
        var dataObject = readDataOptions(index, dataSeries);
       
        return dataObject;
    });

    // draw
    var plot = $.plot($("#placeholder"), dataObjectSet, 
        {
            //series: {
            //    //lines:  {show: true },
            //    //points: {show: true },
            //    bars:   {show: true}
            //},
            grid: { hoverable: true, clickable: true }
        }
    );

    return plot;
}

/*
 * Tooltip & Hover
 */

function showTooltip(x, y, contents) {
    $('<div id="tooltip">' + contents + '</div>').css({
        position          : 'absolute',
        display           : 'none',
        top               : y + 5,
        left              : x + 5,
        border            : '1px solid #fdd',
        padding           : '2px',
        'background-color': '#fee',
        opacity           : 0.80
    }).appendTo("body").fadeIn(200);
}

function onHoverShowTooltip(event, pos, item) {
    if (item) {
        if (previousPoint != item.dataIndex) {
            previousPoint = item.dataIndex;
            
            jQuery("#tooltip").remove();
            var x = item.datapoint[0].toFixed(2),
                y = item.datapoint[1].toFixed(2);

            var label = "";
            if (item.series.label) {
                label = item.series.label + " of ";
            }

            showTooltip(item.pageX, item.pageY,
                        label + x + " = " + y);
        }
    }
    else {
        jQuery("#tooltip").remove();
        previousPoint = null;            
    }
};

/*
 * Tab selection
 */

function onSelectTabUpdate(event, ui) {
    var textarea = "#data-1-textarea";
    var table    = "#data-1-table";
    // table data selected: read from textarea, decode, and apply to table
    if (ui.index == 0) {
        var data = readDataFromTextarea(textarea);
        writeDataToTable(table, data);
    } 
    // textarea data selected: read from table, decode, and apply to textarea
    else {
        var data = readDataFromTable(table);
        writeDataToTextarea(textarea, data);
    }
}

function readDataFromTable(tableEl) {
    var trList = $(tableEl).find('tr').map(function(i,tr) {
        var tdList = $(tr).find('td>input').map(function(j, td) {
            return $(td).val();
        });
        return [tdList.get()];
    });
    return trList.get();
}

function writeDataToTable(tableEl, data) {
    // erase table
    $(tableEl).find('tr').remove();

    console.log(data);

    // add row by row
    $(data).each(function(i, xy) {
        // <td><input type="text" class="x-coord-value" value="$x" /></td>
        // <td><input type="text" class="y-coord-value" value="$y" /></td>
        var xStr = '<td><input type="text" class="x-coord-value" value="' + xy[0] + '" /></td>'
        var yStr = '<td><input type="text" class="y-coord-value" value="' + xy[1] + '" /></td>'
        var newTr = $('<tr>' + xStr + yStr + '</tr>');
        $(tableEl).find('tbody').append(newTr);
    });
}

function readDataFromTextarea(textareaEl) {
    var lines = $(textareaEl).val().split("\n");
    return $(lines).map(function(i, line) {
        return [line.split(" ")];
    }).get();
}

function writeDataToTextarea(textareaEl, data) {
    // erase textarea
    $(textareaEl).empty();

    // write
    var dataStr = $(data).map(function(i, xy) { return xy.join(" ") }).get().join("\n");
    console.log(data);
    console.log(dataStr);
    $(textareaEl).val(dataStr);
}

