from loguru import logger
from sys import stderr
from time import sleep

import settings
from browser import Browser
from wallet import Wallet
from excel import Excel

logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{message}</level>")


def checker(pk: str, excel: Excel, index: str):
    wallet = Wallet(privatekey=pk)
    signature = wallet.sign_message("Thank you for your support of Lista DAO. Sign in to view airdrop details.")
    status, tokens = Browser().get_eligibility(address=wallet.address, signature=signature, index=index)

    excel.edit_table(wallet_data=[wallet.address, status, tokens])
    return {"status": status, "tokens": tokens}


if __name__ == "__main__":
    logger.info(f'Lista Checker\n')
    if settings.PROXY in ["", "http://log:pass@ip:port"]:
        logger.warning(f'You will not using proxies!\n')
        input('\n> Start')

    with open('privatekeys.txt') as f: privatekeys = f.read().splitlines()

    excel = Excel(total_len=len(privatekeys), name="lista_checker")

    total_tokens = 0
    total_eligibility = 0
    for index, pk in enumerate(privatekeys):
        result = checker(pk=pk, excel=excel, index=f'[{index+1}/{len(privatekeys)}]')
        if result["status"] == "Eligible":
            total_eligibility += 1
            total_tokens += result["tokens"]
    eligible_percent = round(total_eligibility / len(privatekeys) * 100, 2)
    total_tokens = round(total_tokens, 2)

    excel.edit_table(wallet_data=[f"Total eligible addresses: {eligible_percent}% [{total_eligibility}/{len(privatekeys)}]"])
    excel.edit_table(wallet_data=[f"Total tokens: {total_tokens} $LISTA"])

    print('\n')
    sleep(0.1)
    logger.success(f'Results saved in "results/{excel.file_name}"\n\nTotal eligibility: {eligible_percent}% [{total_eligibility}/{len(privatekeys)}] with {total_tokens} $LISTA\n\n')
    sleep(0.1)
    input('> Exit')
