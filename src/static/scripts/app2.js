//$(function () {
//	alert("hello Mike!");
//});

//$(function () {

// include app1.js into app2.js file
var imported = document.createElement('script');
imported.src = '/scripts/app1.js';
document.getElementsByTagName('head')[0].appendChild(imported);
	/**
	 * @param [{"name": "Joe", "age": 36}, {"name": "Nick", "age": 12}]
	 */
	function tenantInfoTable(data_json) {		
		//alert("data para:" + data_json);//why display "[obj Object]"?
		var jqTable = $('<table class="table table-bordered"><thead><tr><th>First Name</th><th>Surname</th><th>Gender</th><th>Age</th><th>Phone Number</th><th>Email</th><th>Contact Name</th><th>Contact Phone Number</th><th>Register Date</th></tr></thead><tbody></tbody></table>');
		var jqBody = jqTable.find('tbody');	

		// for (var i = 0; i < data_json.length; i++) {		
			// jqBody.append('<tr><td>' + data_json[i].firstName + '</td><td>' + data_json[i].surname + '</td></tr>');
		// }
				
		$.each(data_json,function(item){
			jqBody.append(
			'<tr><td>' + data_json[item].firstName
			+ '</td><td>' + data_json[item].surname 
			+ '</td><td>' + data_json[item].gender 
			+ '</td><td>'+ data_json[item].age 
			+ '</td><td>' + data_json[item].phoneNumber 
			+ '</td><td>' + data_json[item].email 
			+ '</td><td>' + data_json[item].contactName 
			+'</td><td>' + data_json[item].contactPhoneNumber 
			+ '</td><td>' + data_json[item].registerDate 
			+ '</td></tr>'
			);
		});		
		//$('body').append(jqTable);
		return jqTable;
	}
	
	
	
	
	function tenantProfileEditorTable(tenantKey,data_json) {
		var jqTable = $('<form id="tenantProfileForm" onsubmit="return false;"><table class="table table-bordered"><thead><tr><th>First Name</th><th>Surname</th><th>Gender</th><th>Age</th><th>Phone Number</th><th>Email</th><th>Contact Name</th><th>Contact Phone Number</th><th>Register Date</th><th>Edit</th></tr></thead><tbody></tbody></table></form>');
		var jqBody = jqTable.find('tbody');	
		$.each(data_json,function(item){			
			jqBody.append(
				'<tr><input type="hidden" name="tenant_key" value=' +tenantKey + '>'
				+ '<td><input type="text" readonly="readonly" name="firstName" value=' + data_json[item].firstName 
				+ '></td><td><input type="text" readonly="readonly" name="surname" value=' + data_json[item].surname 
				+ '></td><td><input type="text" readonly="readonly" name="gender" value=' + data_json[item].gender 
				+ '></td><td><input type="text" readonly="readonly" name="age" value='+ data_json[item].age
				+ '></td><td><input type="text" readonly="readonly" name="phoneNumber" value=' + data_json[item].phoneNumber 
				+ '></td><td><input type="text" readonly="readonly" name="email" value=' + data_json[item].email 
				+ '></td><td><input type="text" readonly="readonly" name="contactName" value=' + data_json[item].contactName 
				+ '></td><td><input type="text" readonly="readonly" name="contactPhoneNumber" value=' + data_json[item].contactPhoneNumber 
				+ '></td><td>' + data_json[item].registerDate 
				+ '</td><td class="tenantEditClass" hovertext="click to Edit">'
				+ '<div id="tenantProfileEditorHover"></div>'
				+ '<input type="submit" id="tenantEdit" value="Edit">' 
				+ '</td></tr>'
			);			
		});
		$('body').append(jqTable);
		$('body').append('<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js"></script>');
		$('body').append('<script type="text/javascript" src="/scripts/app1.js"></script>');
		return jqTable;
	}
	
	function roomProfileTable(data_json) {		
		//alert("data para:" + data_json);//why display "[obj Object]"?
		var jqTable = $('<table class="table table-bordered"><thead><tr><th>Number</th><th>Size</th><th>Single Rent</th><th>Double Rent</th><th>Actual Rent</th></tr></thead><tbody></tbody></table>');
		var jqBody = jqTable.find('tbody');	

		// for (var i = 0; i < data_json.length; i++) {		
			// jqBody.append('<tr><td>' + data_json[i].firstName + '</td><td>' + data_json[i].surname + '</td></tr>');
		// }
				
		$.each(data_json,function(item){
			jqBody.append(
			'<tr><td>' + data_json[item].roomNumber
			+ '</td><td>' + data_json[item].size 
			+ '</td><td>' + data_json[item].rentSingle 
			+ '</td><td>'+ data_json[item].rentDouble
			+ '</td><td>' + data_json[item].rentActual 
			+ '</td></tr>'
			);
		});		
		//$('body').append(jqTable);
		return jqTable;
	}
	
	
	
	function roomProfileEditorTable(roomKey,data_json) {
		var jqTable = $('<form id="roomProfileForm" onsubmit="return false;"><table class="table table-bordered"><thead><tr><th>Number</th><th>Size</th><th>Single Rent</th><th>Double Rent</th><th>Actual Rent</th><th>Edit</th><tr></thead><tbody></tbody></table></form>');
		var jqBody = jqTable.find('tbody');
		$.each(data_json,function(item){
			jqBody.append(
				'<tr><input type="hidden" name="room_key" value=' + roomKey 
				+ '><td><input type="text" readonly="readonly" name="number" value=' + data_json[item].roomNumber
				+ '></td><td><input type="text" readonly="readonly" name="size" value=' + data_json[item].size
				+ '></td><td><input type="text" readonly="readonly" name="rentSingle" value=' + data_json[item].rentSingle
				+ '></td><td><input type="text" readonly="readonly" name="rentDouble" value=' + data_json[item].rentDouble
				+ '></td><td><input type="text" readonly="readonly" name="rentActual" value=' + data_json[item].rentActual
				+ '></td><td class = "roomEditClass" hovertext = "Click to Edit">'
				+ '<div id = "roomProfileEditorHover"></div>'
				+ '<input type = "submit" id = "roomEdit" value = "Edit">'												
				+ '</td></tr>'
			);
		});
		$('body').append(jqTable);
		//$('body').append('<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js"></script>');
		$('body').append('<script type="text/javascript" src="/scripts/app1.js"></script>');
		return jqTable;
		
	}

	function registerTenantPage(){
		var jqForm = $('<form id="tenantRegister" onsubmit="return false;">'
		+ '<div>'
		+ '<label for="firstName">First Name: </label>'
		+ '<input id="firstName" type="text" name="firstName" class="required" placeholder="enter first name"/>'
		//+ '<label class="error" for="firstName" id="firstName_error">This field is required.</label>'
		+ '</div>'
		
		+ '<div>'
		+ '<label for="surname">Surname:</label>'
		+ '<input id="surname" type="test" name="surname" class="required" placeholder="enter surname"/>'
		//+ '<label class="error" for="surname" id="surname_error">This field is required.</label>'
		+ '</div>'
		
		+ '<div>'
		+ '<label for="tenant_gender_male">Gender: </label>'
		+ '<input id="tenant_gender_male" type="radio" value="male" name="tenant_gender" class="required"/>'							
		+ '<label for="tenant_gender_male">Male</label>'
		+ '<input id="tenant_gender_female" type="radio" value="female" name="tenant_gender" class="required"/>'
		+ '<label for="tenant_gender_female">Female</label></br>'
		//+ '<label class="error" for="tenant_gender" id="tenant_gender_error"> Please select a gender.</label>'						
		+ '</div>'
		
		+ '<div>'
		+ '<label for="tenant_age">Age:</label>'
		+ '<input id="tenant_age" type="number" name="tenant_age" min="1" max="100" class="required" placeholder="enter age"/>'
		//+ '<label class="error" for="tenant_age" id="tenant_age_error">This field is required.</label>'
		+ '</div>'
		
		+ '<div>'
		+ '<label for="tenant_phoneNumber">Phone Number:</label>'
		+ '<input id="tenant_phoneNumber" type="text" name="tenant_phoneNumber" class="required" placeholder="enter phone number"/>'
		//+ '<label class="error" for="tenant_phoneNumber" id="tenant_phoneNumber_error">This field is required.</label>'
		+ '</div>'
		
		+ '<div>'
		+ '<label> Emergency Contact:</label>'
		+ '<input id="contact_name" type="text" name="contact_name" class="required" placeholder="enter name"/>'
		//+ '<label class="error" for="contact_name" id="contact_name_error">This field is required.</label>'
		+ '</div>'
		
		+ '<div>'
		+ '<label> Emergency Contact PhoneNumber:</label>'
		+ '<input id="contact_phoneNumber" type="text" name="contact_phoneNumber" class="required" placeholder="enter phone number"/>'
		//+ '<label class="error" for="contact_phoneNumber" id="contact_phoneNumber_error">This field is required.</label>'
		+ '</div>'
		
		+ '<div>'
		+ '<label for="registerDate">Register Date:</label>'
		+ '<input id="registerDate" type="date" name="register_date" placeholder="Year-Month-Day">'
		//+ '<label class="error" for="registerDate" id="registerDate_error">This field is required.</label>'
		+ '</div>'	
		
		+ '<div>'						
		+ '<input type="submit" name="submit" class="tenantRegisterButton" id="tenantRegister_btn" value="Submit" />'
		+ '<input type="reset" value="Reset" /></br>'
		+ '</div>'

		+ '</form>');
		$('body').append(jqForm);
		//$('body').append('<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js"></script>');
		
		$('body').append('<script type="text/javascript" src="/scripts/app1.js"></script>');
		
		return jqForm;
	}
	
	function registerRoomPage(){
		var jqForm = $('<form id="roomRegister" onsubmit="return false;">'
		+ '<div>'
		+ '<div>'
		+ '<label for="room_number">Number:</label>'
		+ '<input id="room_number" type="text" name="room_number"/>'
		+ '<label class="error" for="room_number" id="roomNumber_error">This field is required.</label>'
		+ '</div>'
		+ '<div>'
		+ '<label for="room_size">Size:</label>'
		+ '<input id="room_size" type="number" name="room_size"/>'
		+ '<label class="error" for="room_size" id="roomSize_error">This field is required.</label>'
		+ '</div>'
		+ '<div>'
		+ '<label for="room_rent_single">Rent_Single:</label>'
		+ '<input id="room_rent_single" type="number" name="room_rent_single"/>'
		+ '<label class="error" for="room_rent_single" id="rentSingle_error">This field is required.</label>'
		+ '</div>'
		+ '<div>'
		+ '<label for="room_rent_double">Rent_Double:</label>'
		+ '<input id="room_rent_double" type="number" name="room_rent_double"/>'
		+ '<label class="error" for="room_rent_double" id="rentDouble_error">This field is required.</label>'
		+ '</div>'
	
		+ '</div>'		
		+ '<div>'		
		+ '<input type="submit" name="submit" class="roomRegisterButton" id="roomRegister_btn" value="Submit" />'
		+ '<input type="reset" value="Reset"/>'
		+ '</br>'
		+ '<a href="/">Main Page</a>'
		+ '</div>'
		+ '</form>');
		$('body').append(jqForm);
		//$('body').append('<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js"></script>');
		$('body').append('<script type="text/javascript" src="/scripts/app.js"></script>');
		return jqForm;
			
	}
	
	function tenantActivityTable(data_json){
		var jqTable = $('<label>Tenant Activities</label><table class="table table-bordered"><thead><tr><th>Activity Number</th><th>Activity Name</th><th>Activity Date and Time</th></tr></thead><tbody></tbody></table>');
		var jqBody = jqTable.find('tbody');	
				
		$.each(data_json,function(item){
			jqBody.append('<tr><td>' 
			+ data_json[item].activityNumber 
			+ '</td><td>' + data_json[item].activityName 
			+ '</td><td>' + data_json[item].activityDate 
			+ '</td></tr>'
			);
		});		
		return jqTable;
	
	}
	
	function showRoomProfileForm(roomKey,data_json){
		var jqForm = $('<form id="orderRoomForm" onsubmit="return false;"></form>');
		$.each(data_json,function(item){
			jqForm.append(
				'<div>'
				+ '<input type="hidden" name="room_key" value=' + roomKey + ' />'
				+ '</div>'
				// + '<div>'
				// + '<p>Number:' + data_json[item].roomNumber +'</p>'
				// + '</div>'
				+ '<div>'
				+ '<p>Size:'+ data_json[item].size +'</p>'
				+ '</div>'
				+ '<div>'
				// '<input type="checkbox" id = "singleRentCheckBoxId" labelledby="singleRentLable" />'
				+ '<input type = "radio" id = "singleRentRadioId" name = "rent">'
				+ '<label id="singleRentLabel">Single Rent:</label>'						
				+ '<input  type="text" name="room_rentSingle" id="singleRentID" class="rent-input" value=' + data_json[item].rentSingle + ' disabled/>'
				+ '</div>'								
				+ '<div>'							
				//+ '<input type="checkbox" id = "doubleRentCheckBoxId" labelledby="doubleRentLabel" />'
				+ '<input type = "radio" id = "doubleRentRadioId" name = "rent">'
				+ '<label id="doubleRentLabel">Double Rent:</label>'
				+ '<input type="text" name="room_rentDouble" id="doubleRent" class="rent-input" value=' + data_json[item].rentSingle + ' disabled/>'
				+ '</div>'
				//+ '<div>'
				//+ '<input type="submit" value="Order this Room" />'
				//+ '<input type="reset" value="Reset the Order" />'
				//+ '</div>'
			
			
			);
		
		});
		$('body').append(jqForm);
		//$('body').append('<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js"></script>');
		//$('body').append('<script type="text/javascript" src="/scripts/app.js"></script>');
		return jqForm;
	}

	
	function checkinForm(tenantKey,tenant_data,rooms_data){		
		var roomNumberOptions = new Array();
		roomNumberOptions.push('<option value = "title"> Rooms </option>');
		$.each(rooms_data, function(item){
			roomNumberOptions.push('<option value="'+ rooms_data[item].roomKey + '">' + rooms_data[item].roomNumber + '</option>');
		});
		
		var payPeriodOptions = new Array();
		for (var i = 1; i < 13; i++) {		
			payPeriodOptions.push('<option value=' + i +'>' + i + "week" + '</option>');
		}
		
		var jqForm = $('<form id="checkInForm"></form>');
		$.each(tenant_data, function(item){
				jqForm.append(
					'<div>'
					+ '<label> Tenant Name: </label>'
					+ '<label>' + tenant_data[item].firstName + tenant_data[item].surname + '</label>'
					+ '<input type="hidden" name="tenant_key" value=' + tenantKey + ' />'
					+ '</div>'
					
					+ '<label>Please Select a Room:</label>'
					+ '<div  class="selectRoomClass" >'
					//+ '<div id="selectRoomDiv">'
					+ '<select id="selectRoom">'					
					+ '</select>'
					+ '</div>'
					//+ '</div>'
					//+ '<div class = "showRoomInfoClass">'
					//+ '<span id="showRoomInfo"></span>'
					//+ '<div>'
					+ '<span id="showRoomInfo"></span>'
					+ '<div>'
					+ '<label for="tenant_startDate">StartDate:</label>'
					+ '<input id="tenant_startDate" type="date" name="tenant_startDate" placeholder="Year-Month-Day">'
					+ '<label class="error" for="tenant_startDate" id="startDate_error">This field is required.</label>'
					+ '</div>'
					
					+ '<div>'
					+ '<label for="tenant_payPeriod">PayPeriod:</label>'
					+ '</div>'
					+ '<div class = "selectPayPeriodClass">'
					+ '<select id="tenant_payPeriod" name="tenant_payPeriod">'
					+ '</select>'
					+ '</div>'	
					
					+ '<div>'
					+ '<input type="submit" name="submit" class="submitButton" id="submit_btn" value="Check In" >'
					+ '<input type="reset" value="Reset" >'
					+ '</div>'
					
				);

		});
		var selectRoomTag = jqForm.find('.selectRoomClass select');			
		selectRoomTag.html(roomNumberOptions.join(''));

		
		var selectPayPeriodTag = jqForm.find('.selectPayPeriodClass select');
		selectPayPeriodTag.html(payPeriodOptions.join(''));
		
		$('body').append(jqForm);
		//$('body').append('<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js"></script>');
		$('body').append('<script type="text/javascript" src="/scripts/app.js"></script>');		
		return jqForm;
	}
	
	
	
	
	
	
	//function payRentForm(tenantKey,tenant_data){
	function payRentForm(tenantKey,firstName,surname) {
		
		var jqForm = $('<form class="payRentFormClass" id="payRentFormId" ></form>');
		//$.each(tenant_data,function(item){
			jqForm.append(
				
				'<div>'
				+ '<label> Pay Now Form for: </label>'
				+ '<label>' + firstName + '_' + surname + '</label>'
				+ '<input type="hidden" name="tenant_key" value=' + tenantKey + ' />'
				+ '</div>'
				
				+ '<div>'
				+ '<label for="payAmount">Paid Amount: </label>'
				+ '<em>*</em><input id="pay_Amount" type="number" name="payAmount" class="required" placeholder="the amount you want to pay..."/>'
				//+ '<label class="error" for="payAmount" id="payAmount_error">Please type in the amount you want to pay.</label>'
				+ '</div>'
				
				//+ '<div>'
				//+ '<label for="email">Email Address: </label>'
				//+ '<em>*</em><input id="email_address" type="email" name="email" class="required" placeholder="your email address..."/>'
				//+ '<label class="error" for="payAmount" id="payAmount_error">Please type in the amount you want to pay.</label>'
				//+ '</div>'
				
				
				+ '<div>'
				+ '<label for="payDate">Pay Date: </label>'
				+ '<em>*</em><input id="pay_Date" type="date" name="payDate" placeholder="Year-Month-Day" class="required"/>'
				//+ '<em>*</em><input value="2011-12-01" class="validate[required,custom[date]]" type="text" name="payDate" id="pay_Date" />'
				//+ '<label>Name</label>'
				//+ '<em>*</em><input  name="name"  class="required"/>'
				//+ '<label class="error" for="payDate" id="payDate_error">This field is required.</label>'
				+ '</div>'
				//+ '<p><input  id="payRentFormSubmitBtnId" class="submit" type="submit" value="Submit"/></p>'
				//+ '<input  id="payRentFormSubmitBtnId" class="submit" type="submit" value="Submit"/>'
				//+ '<input  id="payRentFormSubmitBtnId" class="submit" type="hidden" value="Submit"/>'
				+ '<div>'		
				//+ '</br>'
				//+ '<a href="/">Main Page</a>'
				+ '</div>'
				);
		//});
		//$('body').append(jqForm);
		//$('body').append('<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js"></script>');
		//$('body').append('<script type="text/javascript" src="/scripts/app.js"></script>');
		//$('body').append('<script type="text/javascript" src="http://jzaefferer.github.com/jquery-validation/jquery.validate.js"></script>');
		//$('body').append('<script type="text/javascript" src="/scripts/jquery.validate.js"></script>');
		
		return jqForm;
	}
	
	
	//check out form
	function checkoutForm(tenantKey,data_json){
		var jqForm = $('<div></div>');
		$.each(data_json, function(item){
			jqForm.append(
				'<div><label>Check out</label>'
				+ '<div><label for="tenant_name">Tenant Name: </label>'
				+  data_json[item].firstName   +  data_json[item].surname  
				+ '<input type="hidden" name="tenant_key" value='
				+  tenantKey
				+ '/></div>'
				+ '<div><label for="tenant_roomNumber">Room Number: </label>'
				+ data_json[item].roomNumber
				+ '</div>'
				+ '<div><label for="tenant_startDate">Start Date: </label>'
				+ data_json[item].startDate
				+ '</div>'
				+ '<div><label for="tenant_livingPeriod">Living Period: </label>'
				+ data_json[item].livingPeriod
				+ '</div>'
				+ '<div><label for="tenant_rent">Rent: </label>'
				+ data_json[item].rent
				+ '</div>'
				+ '<div><label for="tenant_rentRate">Rent Rate: </label>'
				+ data_json[item].rentRate
				+ '</div>'
				+ '<div><label for="tenant_rentPaid">Total Paid Rent: </label>'
				+ data_json[item].totalPaidRent
					
				+ '</div>'
				+ '<div><label for="tenant_unpaidDays">Unpaid Days: </label>'
				+ data_json[item].unpaidDays
				+ '</div>'
				+ '<div><label for="tenant_rentUnpaid">Unpaid Rent: </label>'
				+ data_json[item].unpaidRent
				+ '</div>'
				//+ '<div><a href="/payRent">Pay Now</a></div>'
				// + '<div class=payRentClass>'
				// + '<a id = "payRentBtnId1" href="#" data-tenant-key='
				// + tenantKey + ' data-tenant-firstname='
				// + data_json[item].firstName + ' data-tenant-surname='
				// + data_json[item].surname + ' >Pay Now</a>'
				// + '<div>'
				+ '<div class="checkout"><button data-tenant-key='
				+ tenantKey + ' data-tenant-unpaidrent='
				+ data_json[item].unpaidRent + ' data-tenant-firstname='
				+ data_json[item].firstName + ' data-tenant-surname='
				+ data_json[item].surname
				+ '>Check Out</button></br>'
				+ '</div>'
				+ '<div id="checkoutpayRentId"></div>'
		
		);
		
		
		});
		$('body').append(jqForm);
		//$('body').append('<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js"></script>');
		$('body').append('<script type="text/javascript" src="/scripts/app.js"></script>');
		return jqForm;
	
	
	}
	
	
	
	
	function paymentHistoryTable(data_json){
		var jqTable = $('<label>Payment History</label><table class="table table-bordered"><thead><tr><th>Payment Number</th><th>Pay Date</th><th>Pay Amount</th></tr></thead><tbody></tbody></table>');
		var jqBody = jqTable.find('tbody');	
		$.each(data_json,function(item){
			
			if (data_json[item].totalPaidRent){
				jqBody.append(
				'<tr><td>Total Paid Rent</td><td></td><td>'
				+ data_json[item].totalPaidRent
				+ '</td></tr>'
				);
			}else {
				jqBody.append('<tr><td>' 
					+ data_json[item].paymentNumber 
					+ '</td><td>' + data_json[item].payDate 
					+ '</td><td>' + data_json[item].paidAmount 
					+ '</td></tr>'
				);
			
			}
		});	

		return jqTable;		
	}
	
	
	function tenantHistoryTable(data_json){
		var jqTable = $('<label>Tenant History</label><table class="table table-bordered"><thead><tr><th>Tenant Number</th><th>Tenant name</th><th>Gender</th><th>Age</th><th>Phone Number</th><th>Contact Name</th><th>Contact Number</th><th>Email</th><th>Room Number</th><th>Rent</th><th>Checkin Date</th><th>Checkout Date</th><th>Total Paid Rent</th></tr></thead><tbody></tbody></table>');
		var jqBody = jqTable.find('tbody');	
		$.each(data_json,function(item){
			jqBody.append('<tr><td>' 
				+ data_json[item].tenantNumber 
				+ '</td><td class = "tenantActivityClass" hovertext = "Click to show activities of ' + data_json[item].firstName + "_" + data_json[item].surname 
				+ '">'
				+ '<div id = "tenantActivityHoverDiv"></div>'
				+ '<a id="tenantActivityHrefId" href="#" data-tenant-key =' + data_json[item].tenantKey 
				+ '>' + data_json[item].firstName + "_" + data_json[item].surname
				+ '</a></td><td>' + data_json[item].gender
				+ '</td><td>' + data_json[item].age
				+ '</td><td>' + data_json[item].phoneNumber
				+ '</td><td>' + data_json[item].contactName
				+ '</td><td>' + data_json[item].contactPhoneNumber
				+ '</td><td>' + data_json[item].email
				+ '</td><td>' + data_json[item].roomNumber
				+ '</td><td>' + data_json[item].rent
				+ '</td><td>' + data_json[item].startDate
				+ '</td><td>' + data_json[item].checkoutDate
				+ '</td><td>' + data_json[item].totalPaidRent
				+ '</td></tr>'
			);				
		});	
		$('body').append(jqTable);
	    //$('body').append('<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js"></script>');
		$('body').append('<script type="text/javascript" src="/scripts/app.js"></script>');
		return jqTable;		
	}
	
	
	
	
	
	
	
//});
