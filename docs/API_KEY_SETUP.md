# API key setup

1. Create/sign into a Hugging Face account.
2. Open https://huggingface.co/settings/tokens and create a token with read access.
3. Copy .env.example to .env inside this new project folder.
4. Replace only the HF_TOKEN placeholder with your token. Do not include quote characters unless required by your editor; a normal value is HF_TOKEN=hf_your_token.
5. Run Day 2 after Day 1. python-dotenv loads this file; operating-system environment variables take precedence.

The token is used in stage1.py, day02(), in the Authorization request header:

```python
headers = {"Authorization": f"Bearer {token}"}
```

The token is never sent to the model, SQLite database, MLflow, reports, or public source code. .env is excluded by .gitignore. The shared .env.example contains a placeholder only. Do not add the real .env file to your submitted ZIP. No paid inference call is involved in this design; the token authenticates dataset retrieval. Public dataset access may also work without a token, but this project intentionally demonstrates authenticated requests.

401/403 means access failed; verify the token and account permissions. 429 means rate limiting; the client respects Retry-After and retries. Do not paste the key into a chat or a report to troubleshoot it.

The default API source is codeparrot/apps, config all, split train. Day 2 lists available split/config combinations if these defaults become unavailable. Dataset rows are paginated at up to 100 per call. The raw snapshot contains response bodies and checksums, not request headers.
