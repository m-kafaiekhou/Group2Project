

Testing
---------------

One of the most important parts about any project is unittests which is performed by the help of TestCase. 
the project is tested to find any buggs in code or find the changes in project more easily. 
best practice here is the test coverage of 95%.

An example:

..  code-block:: python

    def test_sales_by_time_of_day_data_start_date_smaller(self):
        self.client.login(phone_number='09030001122', password='1X<ISRUkw+tuK')
        start_date = "2023-8-10"
        end_date = "2023-8-20"
        url = reverse("daily-time-sale")
        data = {'start_date': start_date, 'end_date': end_date}
        response = self.client.get(url, data=data)

        expected_data = {
            "title": f"Sales by Time of Day Between {start_date} and {end_date}",
            "data": {
                "labels": [],
                "datasets": [{
                    "label": "Amount (T)",
                    'borderColor': '#d048b6',
                    'borderWidth': 2,
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'pointBackgroundColor': '#d048b6',
                    'pointBorderColor': 'rgba(255,255,255,0)',
                    'pointHoverBackgroundColor': '#d048b6',
                    'pointBorderWidth': 20,
                    'pointHoverRadius': 4,
                    'pointHoverBorderWidth': 15,
                    'pointRadius': 4,
                    "data": [],
                }]
            }
        }
        self.assertAlmostEqual(response.json(), expected_data)
    

Which tests the sale by time of day chart data between two dates. start date and end date...

coverage: a testing tool for django which tests the test files and returns reporsts in html, or on terminal.

**In order to test using coverage:**

    ``coverage run manage.py test -v 2``