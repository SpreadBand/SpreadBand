/*
Copyright (c) 2003-2010, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/


CKEDITOR.editorConfig = function( config )
{
    // Define changes to default configuration here. For example:
    config.language = 'fr';
    config.toolbar =
	[
	    ['Source', '-', 'Undo', 'Redo'],
	    ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
	    ['NumberedList','BulletedList','-','Outdent','Indent'],
	    ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock']
	];
};
