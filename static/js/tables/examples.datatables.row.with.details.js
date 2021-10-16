
(function( $ ) {

	'use strict';

	var datatableInit = function() {
		var $table = $('#datatable-gestionvuelos');

		// format function for row details
		var fnFormatDetails = function( datatable, tr ) {
			var data = datatable.fnGetData( tr );

			return [
				'<table class="table mb-none">',
					'<tr class="b-top-none">',
						'<td><label class="mb-none">Id Avión</label></td>',
						'<td> fes2653 </td>',
					'</tr>',
					'<tr class="b-top-none">',
						'<td><label class="mb-none">Fecha de salida</label></td>',
						'<td> 12/10/2021 </td>',
					'</tr>',
					'<tr>',
						'<td><label class="mb-none">Hora de salida</label></td>',
						'<td>14:10:00</td>',
					'</tr>',
					'<tr>',
						'<td><label class="mb-none">Hora de llegada</label></td>',
						'<td>14:40:00</td>',
					'</tr>',
					'<tr>',
						'<td><label class="mb-none">Cantidad de pasajeros</label></td>',
						'<td>70</td>',
					'</tr>',
				'</div>'
			].join('');
		};

		// insert the expand/collapse column
		var th = document.createElement( 'th' );
		var td = document.createElement( 'td' );
		td.innerHTML = '<i data-toggle class="fa fa-plus-square-o text-primary h5 m-none" style="cursor: pointer;"></i>';
		td.className = "text-center";

		$table
			.find( 'thead tr' ).each(function() {
				this.insertBefore( th, this.childNodes[0] );
			});

		$table
			.find( 'tbody tr' ).each(function() {
				this.insertBefore(  td.cloneNode( true ), this.childNodes[0] );
			});

		// initialize
		var datatable = $table.dataTable({
			aoColumnDefs: [{
				bSortable: false,
				aTargets: [ 0 ]
			}],
			aaSorting: [
				[1, 'asc']
			]
		});

		// add a listener
		$table.on('click', 'i[data-toggle]', function() {
			var $this = $(this),
				tr = $(this).closest( 'tr' ).get(0);

			if ( datatable.fnIsOpen(tr) ) {
				$this.removeClass( 'fa-minus-square-o' ).addClass( 'fa-plus-square-o' );
				datatable.fnClose( tr );
			} else {
				$this.removeClass( 'fa-plus-square-o' ).addClass( 'fa-minus-square-o' );
				datatable.fnOpen( tr, fnFormatDetails( datatable, tr), 'details' );
			}
		});
	};

	$(function() {
		datatableInit();
	});

}).apply( this, [ jQuery ]);