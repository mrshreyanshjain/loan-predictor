Firstly, there is an additional method that I had to add in the scikit-learn's library. If you get any
error regarding the "predict2" method then just simply copy and replace the "_base.py" to the original file.


Here are the steps to use the Model.
1. Run the flask server from "mainServer.py".
        (server.py and testServer.py were used for trail and testing, should not use them)

2. Open the server in the browser.

3. Select the CSV file from "./loan_data/test_data.csv" or any other CSV file having the same column names
    as the "loan_data.csv" has. (You can leave the Last "Loan Status" Column)

4. Now just predict and download your CSV file with result in it :)