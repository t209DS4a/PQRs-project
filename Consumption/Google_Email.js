function gen_rad_number() {
  /**
   * START GATHERING INFORMATION
   * Here we start Gathering the information from the Answers' Sheet
   */
  var ss = SpreadsheetApp.openById(
    "1qCn8flw5T2hFzn6YHBXHVjYyi0f7WttleD47lh276PY"
  );
  var sheetAns = ss.getSheetByName("responses_for_df");
  var sheetDB = ss.getSheetByName("ibage_big_dt");

  /** Get last row number */
  var Alast = sheetAns.getRange("A:A").getValues().filter(String).length;

  /** Get values */
  var timestamp = sheetAns.getRange("A" + Alast).getValue();
  var firstName = sheetAns.getRange("B" + Alast).getValue();
  var lastName = sheetAns.getRange("C" + Alast).getValue();
  var descriptionISUE = sheetAns.getRange("D" + Alast).getValue();
  var docNumber = sheetAns.getRange("E" + Alast).getValue();
  var email = sheetAns.getRange("F" + Alast).getValue();

  /** Generate num Radix Number  */
  var today = new Date();
  var radDate = new Date(timestamp);
  var start = new Date(radDate.getFullYear(), 0, 0);
  var diff =
    today -
    start +
    (start.getTimezoneOffset() - today.getTimezoneOffset()) * 60 * 1000;
  var oneDay = 1000 * 60 * 60 * 24;
  var dayofYear = String(Math.floor(diff / oneDay)).padStart(3, "0");
  today.setHours(0, 0, 0, 0);
  var milisecDiff = String(radDate - today);
  var milisecDiff = milisecDiff.substring(milisecDiff.length - 3);

  var radNumber =
    radDate.getFullYear() + "-" + dayofYear + milisecDiff.substring(1, 4);

  /** OTHER VARIABLES */
  var glb_estado_id = "Digitalizado";
  var fechaRad =
    radDate.getFullYear() +
    "-" +
    String(radDate.getMonth()).padStart(2, "0") +
    "-" +
    String(radDate.getDate()).padStart(2, "0");

  /** Get last row number on big table */
  var Alast2 = sheetDB.getRange("A:A").getValues().filter(String).length;
  var fullName = firstName + " " + lastName;
  var nextCell = Number(Alast2 + 1);

  sheetDB.getRange("A" + nextCell).setValue(Alast2);
  sheetDB.getRange("B" + nextCell).setValue(glb_estado_id);
  sheetDB.getRange("AC" + nextCell).setValue(radNumber);
  sheetDB.getRange("Q" + nextCell).setValue(docNumber);
  sheetDB.getRange("AD" + nextCell).setValue(fechaRad);
  sheetDB.getRange("BV" + nextCell).setValue(docNumber);
  sheetDB.getRange("BF" + nextCell).setValue(fullName);
  sheetDB.getRange("CL" + nextCell).setValue(docNumber);
  sheetDB.getRange("EC" + nextCell).setValue(radNumber);
  sheetDB.getRange("EI" + nextCell).setValue("TEST");

  /** ------------------------------------Email Structure--------------------------------*/
  var subject = "PQR Created Succesfully";

  var htmlBody2 = HtmlService.createHtmlOutput(
    '<html style="background: #fff !important;"><meta name="color-scheme" content="only"><body><div id="app" style="font-size: 14px;font-family: Helvetica Neue, Helvetica, Arial, sans-serif;color: #101010;overflow-x: hidden;"><div style="display: flex;-webkit-box-orient: vertical;-webkit-box-direction: normal; background: #fff;"><div class="page-container" style="width: 100%; margin: auto;"><div class="page-content">' +
      '<img src="https://www.correlation-one.com/hubfs/c1logo_color.png" style = "width: 370px; display: block; margin-left: auto;margin-right: auto;margin-top: 50px;" ><div class="wrapper slogan-wrapper" style="text-align: center; font-size: 12px; color: #333; margin-top: 5px; margin-left: 12px;"><br><br><div style="font-size: 24px; font-weight: Bold;">TEAM 209</div></div><br>' +
      '<div class="wrapper form-wrapper"style="padding: 30px 25px;background-color: #fff;border-radius: 3px;text-align: center;"><h4 style="text-align: left;">' +
      "Hi  <strong>" +
      fullName +
      "!" +
      "</strong></h4></div>" +
      '<p style="padding: 10px 25px;" >The PQRS was successfully created under the Filing number (RAD): <strong>' +
      radNumber +
      "</strong>" +
      "<br><br><br><br>Kindly,<br><strong>TEAM 209</strong>" +
      "</p></div></div></div></div></body ></html >"
  );

  var targetEmail = email; //'camilosernar@outlook.com'
  var body = "";

  MailApp.sendEmail({
    to: targetEmail,
    subject: subject,
    body: body,
    htmlBody: htmlBody2.getContent(),
  });
}
