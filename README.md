<h1>Algo Trader</h1>
This repo aims to make trades using algorithms. Currently working with Charles Schwab API. Extensible to use other APIs. Trading is hosted on GCP (or locally).

<h2>Setup</h2>
To get started you will need the following:
<ul>
<li>Python 3.11 or newer</li>
<li>Docker</li>
<li>Terraform CLI</li>
<li>Google Cloud CLI</li>
</ul>
If you only want to run locally, you do not need the Terraform CLI or the Google Cloud CLI.

To start and get the application running locally please refer the the README in local_testing_example. Once you have the application running locally you can follow the steps below to deploy the app to GCP.

<h2>GCP Deployment</h2>
To deploy to GCP you first need:
<ul>
<li>A Google Cloud account and a project</li>
<li>Terraform CLI</li>
</ul>
Be sure to download the GCP CLI and Terraform CLI before moving on. 

[GCP CLI Docs](https://cloud.google.com/sdk/docs/install#linux)

[Terraform CLI Docs](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

Once you have logged in, in your GCP project navigate to the Secret Manager service. From there add 3 secrets:
<ul>
<li>schwab-app-key</li>
<li>schwab-secret-key</li>
<li>schwab-tokens</li>
</ul>
These secrets are referenced by the cloud run service our app will be running on. Add your app key, secret key, and tokens (generated when we ran locally) to each of the secrets in GCP. Be sure to make your tokens.json flat when adding it to the secret otherwise GCP will interperet "\n" newlines to be part of the token. Example:

```
{"access_token_issued": "2025-01-10T21:35:07.880308+00:00","refresh_token_issued": "2025-01-10T21:35:07.880308+00:00"...}
```
Once your secrets are ready, navigate to the Artifact Registry service in GCP. From there create a new repository called "algo-trading". This is where we will be uploading our docker image to run on cloud run. Before uploading the image, update refresh_image.sh to target your project name:

```
docker image rm us-central1-docker.pkg.dev/<your_project-name>/algo-trading/algo-trader
docker buildx build --platform linux/amd64 -t algo-trader .
docker tag algo-trader:latest \us-central1-docker.pkg.dev/<your_project-name>/algo-trading/algo-trader
gcloud container images delete us-central1-docker.pkg.dev/<your_project-name>/algo-trading/algo-trader
docker push us-central1-docker.pkg.dev/<your_project-name>/algo-trading/algo-trader
```

Now from the root directory run:

```
bash refresh_image.sh
```

This will build the docker image and push it to the artifact registry we just created in GCP. Now that we have our secrets and docker image set up we are about ready to deploy to GCP! In gcp_deplopyment/variables.tf, be sure to change the default values of the variables to your project_id, bucket_name, and region you are deploying to (if you want to deploy to a different region be sure to change the region in refresh_image.sh as well). Your bucket name must be something globally unique otherwise terraform will throw an error! Good practice is to name it and put random numbers on the end of the name like so:

```
variable "project_id" {
    default = "schwab-algo-trading"
}

variable "region" {
    default = "us-central1"
}

# don't use this name it's taken
variable "bucket_name" {
    default = "trader-bucket-61423"
}
```

Once you've edited the variables.tf file it's finally time to deploy! Navigate to the gcp_deployment directory and run:

```
terraform init
terraform plan
terraform apply
```

If everything is functioning correctly terraform should have passed the plan stage and applied the resources described in the main.tf file to your GCP project. You should now be able to find your bot running by navigating through the GCP console to Cloud Run and clicking on the link for your service.
<br>
<br>
![Stock Trader](assets/stock_bot.png)

<h2>Maintenance</h2>

<h3>Tokens</h3>
Every week your Schwab tokens will expire. Once a week you will have to replace the schwab_tokens secret with a new schwab_tokens secret with the updated tokens.json. You can generate new tokens by using get_tokens.py in local_testing_example.

<h3>Pricing</h3>
With the current terraform setup, the cloud run instance will scale down to 0 minimum instances outside of market hours and up to 1 during market hours. If you leave the infrastructure up it may run you about 100 dollars per month. 