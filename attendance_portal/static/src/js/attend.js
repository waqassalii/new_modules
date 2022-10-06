$( document ).ready(function() {

    $(".checkin-icon").click(function () {
    if ("geolocation" in navigator){ //check geolocation available
		//try to get user current location using getCurrentPosition() method
		navigator.geolocation.getCurrentPosition(function(position){
				var latitude = position.coords.latitude;
				var longitude = position.coords.longitude;
				console.log("qwe");
				$.ajax({
                    type: "POST",
                    dataType: 'json',
                    url: '/attendance/checkin',
                    contentType: "application/json; charset=utf-8",
                    data: JSON.stringify({'latitude': latitude,'longitude':longitude}),
                    success: function () {
                        location.reload();
                    },
                    error: function (data) {
                        console.error("ERROR ", data);
                    },
                });
			});
	}else{
		console.log("Browser doesn't support geolocation!");
		var latitude = ''
		var longitude = '';
	}



});

$(".checkout-btn").click(function () {
    if ("geolocation" in navigator){ //check geolocation available
		//try to get user current location using getCurrentPosition() method
		navigator.geolocation.getCurrentPosition(function(position){
				var latitude = position.coords.latitude;
				var longitude = position.coords.longitude;
				console.log("qwe");
				$.ajax({
                    type: "POST",
                    dataType: 'json',
                    url: '/attendance/checkout',
                    contentType: "application/json; charset=utf-8",
                    data: JSON.stringify({'latitude': latitude,'longitude':longitude}),
                    success: function () {
                        location.reload();
                    },
                    error: function (data) {
                        console.error("ERROR ", data);
                    },
                });
			});
	}else{
		console.log("Browser doesn't support geolocation!");
		var latitude = ''
		var longitude = '';
	}

});
});
