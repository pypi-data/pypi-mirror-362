import requests
from datetime import datetime, timedelta

class PaymentChecker:
    def __init__(self, config):
        if not config.get('auth_username'):
            raise ValueError('auth_username harus diisi')
        if not config.get('auth_token'):
            raise ValueError('auth_token harus diisi')
        self.config = {
            'auth_username': config.get('auth_username'),
            'auth_token': config.get('auth_token')
        }

    def check_payment_status(self, reference, amount):
        try:
            if not reference or not amount or amount <= 0:
                raise ValueError('Reference dan amount harus diisi dengan benar')

            url = 'http://152.42.183.197:6969/api/mutasi'
            headers = {
                'Content-Type': 'application/json'
            }
            payload = {
                'auth_username': self.config['auth_username'],
                'auth_token': self.config['auth_token']
            }
            response = requests.post(url, json=payload, headers=headers)

            if not response.ok:
                raise Exception(f"HTTP error: {response.status_code}")
            data = response.json()
            if not data.get('status') or not data.get('data'):
                raise Exception('Response tidak valid dari server')

            transactions = data['data']
            matching_transactions = []
            now = datetime.now()
            for tx in transactions:
                try:
                    tx_amount = int(tx['amount'])
                    tx_date = datetime.strptime(tx['date'], '%Y-%m-%d %H:%M:%S')
                    time_diff = (now - tx_date).total_seconds()
                    if (
                        tx_amount == amount and
                        tx.get('type') == 'CR' and
                        time_diff <= 600
                    ):
                        matching_transactions.append(tx)
                except Exception:
                    continue

            if matching_transactions:
                latest_transaction = max(
                    matching_transactions,
                    key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S')
                )
                return {
                    'success': True,
                    'data': {
                        'status': 'PAID',
                        'amount': int(latest_transaction['amount']),
                        'reference': latest_transaction.get('issuer_reff', reference),
                        'date': latest_transaction['date'],
                        'brand_name': latest_transaction.get('brand_name'),
                        'buyer_reff': latest_transaction.get('buyer_reff')
                    }
                }

            return {
                'success': True,
                'data': {
                    'status': 'UNPAID',
                    'amount': amount,
                    'reference': reference
                }
            }
        except Exception as error:
            return {
                'success': False,
                'error': f'Gagal cek status pembayaran: {str(error)}'
            }