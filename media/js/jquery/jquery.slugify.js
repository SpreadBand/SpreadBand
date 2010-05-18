jQuery.fn.slugify = function(obj)
{
    jQuery(this).data('obj', jQuery(obj));
    jQuery(this).keyup(function()
	{
	    var obj = jQuery(this).data('obj');
	    var slug = jQuery(this).val().replace(/[\'\s]+/g,'-').replace(/[éèê]/g, 'e').replace(/[âà]/g, 'a').replace(/[ç]/g, 'c').replace(/[^a-zA-Z0-9\-]/g,'').toLowerCase();
	    obj.val(slug);
	}
    );
}
