from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
import os

from login import init_login

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET", "defaultsecret")

os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)
db_path = os.path.join(app.root_path, "instance", "mileage.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
init_login(app)

CENTRAL = pytz.timezone("America/Chicago")
LEASE_START = datetime(2024, 9, 8)
STARTING_MILES = 17
MONTHLY_ALLOWANCE = 1000

class MileageEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, nullable=False)
    odometer = db.Column(db.Integer, nullable=False)

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        year = int(request.form['year'])
        month = int(request.form['month'])
        odometer = int(request.form['odometer'])

        # Calculate last day of given month
        first_day_next = datetime(year, month, 28) + relativedelta(days=4)
        last_day = first_day_next - relativedelta(days=first_day_next.day)

        entry = MileageEntry(entry_date=last_day.date(), odometer=odometer)
        db.session.add(entry)
        db.session.commit()
        return redirect('/')

    # Get entries, most recent first
    entries = MileageEntry.query.order_by(MileageEntry.entry_date.desc()).all()

    data = []
    for entry in entries:
        months_passed = (entry.entry_date.year - LEASE_START.year) * 12 + (entry.entry_date.month - LEASE_START.month) + 1
        allowed = months_passed * MONTHLY_ALLOWANCE
        odometer_adj = entry.odometer - STARTING_MILES
        off_target = odometer_adj - allowed
        data.append({
            'date': entry.entry_date.strftime('%Y-%m-%d'),
            'odometer': entry.odometer,
            'allowed': allowed + STARTING_MILES,
            'off_target': off_target
        })

    # Sort separately for the chart
    chart_data = sorted(data, key=lambda x: x['date'])

    return render_template("index.html", data=data, chart_data=chart_data, current_year=datetime.now().year)

# Run the app locally (not needed in Docker production)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
