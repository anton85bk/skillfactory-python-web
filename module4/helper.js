function hello_world() {
	alert("Hello world!")
}
function get_data_from_json() {
/*                      forecasts_url = "http://localhost:8080/api/forecasts"; */
	forecasts_url = "https://sf-pyw.mosyag.in/m04/api/forecasts";
	json = $.getJSON(forecasts_url, function(data) {
					set_content_in_divs(data["prophecies"])
				 }
			);
}
function set_content_in_divs(paragraphs) {
	$.each(paragraphs, function(i, d) {
				p = $("#p-" + i);
				p.html("<p class=\"p_forecast\">" + d + "</p>");
			   }
	      );
}
