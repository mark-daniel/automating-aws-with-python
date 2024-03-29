import boto3
import click
from botocore.exceptions import ClientError

session = boto3.Session(profile_name='markpav')
s3 = session.resource('s3')

@click.group()              #a decorator
def cli():
    "Webotron deploys websites to AWS"
    pass

@cli.command('list-buckets')
def list_buckets():         #create function
    "List all s3 buckets"   #Known as a doc string
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command("list-bucket-objects") #give it a command name with dash
@click.argument('bucket')
def list_bucket_objects(bucket):
    "List objects in an s3 bucket"
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)

@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    "Create and configure S3 bucket"
    s3_bucket = None
    
    try:
        s3_bucket = s3.create_bucket(Bucket=bucket)
            # To create buckets outside of us-east-1
            #     CreateBucketConfiguration=
            #     {'LocationConstraint': session.region_name}
            # )
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket = s3.Bucket(bucket)
        else:
            raise e

    policy = """
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::%s/*"
            }
        ]
    }
    """ %s3_bucket.name
    policy = policy.strip()

    pol = s3_bucket.Policy()
    pol.put(Policy=policy)

    ws = s3_bucket.Website()
    ws.put(WebsiteConfiguration={
        'ErrorDocument': {
            'Key': 'error.html'
        },
        'IndexDocument': {
            'Suffix': 'index.html'
        }
    })

    return

if __name__ == '__main__':
    cli()          #call function
