import boto3
import click

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

if __name__ == '__main__':
    cli()          #call function
