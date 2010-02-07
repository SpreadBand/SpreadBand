/*
 * A layout editor based on 960GS
 * (jQuery version)
 */
function Grider()
{
    var selected = null;

    $(".container_12").dblclick(on_dblclick);
    //$("div[class^='grid_']").map(resizehandle);
    //    $("div[class^='grid_']").resizable();

    $(".container_12").click(select);

    maketip();

    $("#grider_grow").click(grow);
    $("#grider_shrink").click(shrink);
    $("#grider_add").click(add);
    $("#grider_del").click(del);

    //$(".container_12 div[class^='grid_']").hover(on_hoverin, on_hoverout);
    //$(".container_12 div[class='grider_temp']").hover(null, on_mouseout);
    //$(".container_12 div[class^='grid_']").dblclick(on_select);
    //$(".container_12 div[class^='grid_']").bind("click", on_select);

    function select(event) {
	var element = jQuery(event.target);
	selected = element;
	$("#grider_selected").val(selected.get(0).nodeName);

	return true;
    }

    function grow(event) {
	if ( selected == null )
	    return false;
	changeSizeRelative(selected, +1);
    }

    function shrink(event) {
	if ( selected == null )
	    return false;
	changeSizeRelative(selected, -1);
    }

    function add(event) {
	if ( selected == null )
	    return false;

	var size = parseInt(jQuery("#grider_size").val());

	if ( isNaN(size) )
	    return false;

	if ( ! appendGridTo(selected, size) )
	    return false;

	return false;
    }

    function maketip()
    {
	r = jQuery(".container_12 div[class^='grid_']").qtip(
	    {
		content: jQuery("#grider_editor"),
		show: {
		    solo: true,
		    when: {
			event: 'click' } },
		hide: {
		    when: 'click',
		    fixed: true },
		position: {
		    adjust: {
			screen: true },
			corner: {
			    target: 'topMiddle',
			    tooltip: 'bottomMiddle'
			}
		},
		style: { tip: 'bottomMiddle' }
	    }
	);

	return r;

    }

    function del(event) {
	if ( selected == null )
	    return false;

	deleteGrid(selected);

	return false;

    }

    /* Callback when selecting an element */
    function on_dblclick(event)
    {
	var size = parseInt(jQuery("#grider_size").val());

	var element = jQuery(event.target);

	if ( isNaN(size) )
	    return false;

	if ( ! appendGridTo(element, size) )
	    return false;

	return false;
    }

    function deleteGrid(element)
    {
	var prev_el = element.prev();
	var next_el = element.next();

	element.remove();

	if ( prev_el )
	    fixAlpha(prev_el);

	if ( next_el )
	    fixOmega(element);

    }

    /* Append a grid element to another grid element */
    function appendGridTo(element, size)
    {
	/* Check if clear div is here, add it if needed */
	if ( ! hasClear(element) )
	    addClear(element);

	var lastchild = element.children().last();

	/* Check if we have enough room to add our grid */
	if ( freeSpaceAtRow(lastchild) < size )
	    return false;

	/* Append our grid before the clear div */
	return insertGridBefore(lastchild, size);
    }

    /* Insert a grid of the given size before element */
    function insertGridBefore(element, size)
    {
	var newgrid = jQuery("<div>newgrid</div>");
	newgrid.addClass("grid_" + size);
	newgrid.attr("style", "background-color: #abc; opacity: 0.5; height: 100%;");
	element.before(newgrid);

	fixAlpha(newgrid);
	fixOmega(newgrid);

	return newgrid;
    }

    /* Fix omega class attribution */
    function fixOmega(element)
    {
	var prev_el = element.prev();
	if ( prev_el.length == 0 || prev_el.hasClass("omega") )
	{
	    prev_el.removeClass("omega");
	    element.addClass("omega");
	}
    }

    /* Fix omega class attribution */
    function fixAlpha(element)
    {
	var prev_el = element.prev();
	var next_el = element.next();

	/* Fix alpha class attribution */
	if ( prev_el.length == 0 || next_el.hasClass("alpha") )
	{
	    next_el.removeClass("alpha");
	    element.addClass("alpha");
	}
    }

    /* Check if a grid has a clear div at the end */
    function hasClear(element)
    {
	var lastChild = element.children().last();
	return(lastChild.hasClass("clear"));
    }

    /* Add a div with clear class at the end of a grid */
    function addClear(element)
    {
	var newclear = jQuery("<div></div>");
	newclear.addClass("clear");
	element.append(newclear);
    }

    /*
     * Size related methods
     */

    /* Return the size of the parent of a grid element */
    function parentSize(element)
    {
	var parent = jQuery(element.parent().get(0));
	return sizeOfGrid(parent);
    }

    /* Get the size of a grid element */
    function sizeOfGrid(element)
    {
	if ( element.hasClass("container_12") )
	    return 12;
	else if ( element.hasClass("grid_12") )
	    return 12;
	else if ( element.hasClass("grid_11") )
	    return 11;
	else if ( element.hasClass("grid_10") )
	    return 10;
	else if ( element.hasClass("grid_9") )
	    return 9;
	else if ( element.hasClass("grid_8") )
	    return 8;
	else if ( element.hasClass("grid_7") )
	    return 7;
	else if ( element.hasClass("grid_6") )
	    return 6;
	else if ( element.hasClass("grid_5") )
	    return 5;
	else if ( element.hasClass("grid_4") )
	    return 4;
	else if ( element.hasClass("grid_3") )
	    return 3;
	else if ( element.hasClass("grid_2") )
	    return 2;
	else if ( element.hasClass("grid_1") )
	    return 1;
	else
	    return 0;
    }

    /* Return the space used inside a grid at the corresponding row */
    function usedSpaceAtRow(element)
    {
	var size = 0;
	var parent = jQuery(element.parent().get(0));

	/* Calculate space until previous clear div or beginning */
	element.prevUntil("div[class='clear']").each(function(i, child) {
							 size += sizeOfGrid(jQuery(child));
						     });

	/* Calculate space until next clear div or end */
	element.nextUntil("div[class='clear']").each(function(i, child) {
							 size += sizeOfGrid(jQuery(child));
						     });

	/* Add our space */
	size += sizeOfGrid(element);

	return size;
    }

    function largestUsedSpace(element)
    {
	var maxsize = 0;
	element.children("div[class='clear']").each(function(i, child) {
							maxsize = Math.max(maxsize, usedSpaceAtRow(jQuery(child)));
						    });

	return maxsize;
    }

    /* Return the free space inside a grid element at the corresponding row */
    function freeSpaceAtRow(element)
    {
	return Math.max(0, parentSize(jQuery(element)) - usedSpaceAtRow(jQuery(element)));
    }

    /* Change the size of a grid, relatively */
    function changeSizeRelative(element, delta)
    {
	var size = sizeOfGrid(element);
	return changeSize(element, size+delta);
    }

    /* Change the size of a grid, absolutely */
    function changeSize(element, newsize)
    {
	var size = sizeOfGrid(element);
	var row_freespace = freeSpaceAtRow(element);
	var largest_row = largestUsedSpace(element);

	if ( (newsize < 1) || (newsize < largest_row) )
	    return false;

	if ( ((row_freespace + size) - newsize) < 0 )
	{
	    // alert(((parent_freespace + size) - newsize));
	    // alert("oldsize" + size);
	    // alert("newisze" + newsize);

	    return false;
	}

	element.removeClass("grid_" + size).addClass("grid_" + newsize);

	return true;
    }
}

jQuery.fn.Grider = Grider

