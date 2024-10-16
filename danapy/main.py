from models.error import DanaUsageError
from ext.autosave import DaNAAutosave
from api.client import DanaClient
import uuid
from flask import Blueprint

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/main')
def main_function():
    # kode di sini
    pass

class DANA(object):
    def __init__(self, *args, **kws):
        self.opt = {
            'save_auth': True,
            'base_url': 'https://api.dana.id/',
            'app_id': 'YOUR_APP_ID',
            'app_version': 'YOUR_APP_VERSION',
            'os_name': 'Android',
            'os_version': '8.1.0',
            'mac_address': '02:00:00:44:55:66',
            'device_id': str(uuid.uuid4()),
            'notification_id': 'FCM|f4OXYs_ZhuM:APA91bGde-ie2YBhmbALKPq94WjYex8gQDU2NMwJn_w9jYZx0emAFRGKHD2NojY6yh8ykpkcciPQpS0CBma-MxTEjaet-5I3T8u_YFWiKgyWoH7pHk7MXChBCBRwGRjMKIPdi3h0p2z7',
        }
        if len(args) > 0:
            raise DanaUsageError('Please use `key arguments` instead of DANA(%s)' % (','.join(['%r' % arg for arg in args])))
        self.opt.update(kws)
        self.client = DanaClient(**self.opt)
        self.auto_save = DaNAAutosave(**self.opt)
        self.client.onValidLogin = self.onValidLogin
        self.client.onValidSecurityCode = self.onValidSecurityCode
        self.client.checkOnSavedCredential = self.auto_save.checkOnSavedCredential

        self.settings = {}

    def onValidLogin(self, res):
        settings = {
            'mobile': res.mobile,
            'email': res.email,
            'fullName': res.fullName,
            'isEmailVerified': res.isEmailVerified,
            'isSecurityCodeSet': res.isSecurityCodeSet,
            'authToken': res.updateAccessToken,
        }
        self.settings.update(settings)
        if self.opt.get('save_auth', False):
            print('Identity saved.')
            self.auto_save.createNewOrUpdateExist(str(self.phone_number), self.settings)
        else:
            print('Warning: Identity of the account WILL not saved.')

    def onValidSecurityCode(self, res, securityCode):
        settings = {
            'token': res.token,
            'tokenSeed': res.tokenSeed,
            'authToken': res.updateAccessToken,
            'securityCode': securityCode,
        }
        self.settings.update(settings)
        if self.opt.get('save_auth', False):
            print('Credential saved.')
            self.auto_save.createNewOrUpdateExist(str(self.phone_number), self.settings)
        else:
            print('Warning: Auto save token is disabled. Please get your login token manually.')

    def getAccountSaved(self, phone_number):
        # alpha
        pass

    def login(self, phone_number=None, token=None, forceRenew=False):
        if token:
            self.settings = self.auto_save.resolveSettingsFromToken(token)
            if self.settings == {}:
                print('Warning: Identity can\'t be resolved. You can use getBalanceModel')
            return self.client.loginWithToken(token)
        elif phone_number:
            # manage to load from saved session instead of creating new one ;)
            self.phone_number = phone_number
            self.settings = self.auto_save.resolveSavedAccount(phone_number)
            if self.settings.get('token', None) and (~forceRenew):
                print('Info: Successfully retrieve token from saved file!')
                return self.client.loginWithToken(self.settings.get('token', ''))
            else:
                print('Info: Token not found, attempt to login now...')
                return self.client.login2FA(phone_number)

    def verifyLogin2FA(self, refId, verficationCode, phone_number):
        # verificationCode equals otpCode
        return self.client.verifyLogin2FA(refId, verficationCode, phone_number)

    def loginSecurityCode(self, pin_code, updateAccessToken):
        return self.client.loginSecurityCode(pin_code, updateAccessToken)

    def getBudget(self, *args, **kws):
        return self.client.getBudget(*args, **kws)

    def getFrontModel(self, *args, **kws):
        return self.client.getFrontModel(*args, **kws)

    def generateTrxId(self, *args, **kws):
        return self.client.generateTrxId(*args, **kws)

    def transferDANABalance(self, *args, **kws):
        return self.client.transferDANABalance(*args, **kws)

    def logout(self, *args, **kws):
        return self.client.logout(*args, **kws)

    def getAllNotification(self, *args, **kws):
        return self.client.getAllNotification(*args, **kws)

    def getUnreadNotification(self, *arg, **kws):
        return self.client.getUnreadNotification(*arg, **kws)

    def getWalletTransaction(self, *arg, **kws):
        return self.client.getWalletTransaction(*arg, **kws)