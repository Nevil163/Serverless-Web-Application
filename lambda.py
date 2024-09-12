import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentRecords')

def lambda_handler(event, context):
    if event['httpMethod'] == 'POST':
        # Create a new student record
        student = json.loads(event['body'])
        table.put_item(Item=student)
        return {
            'statusCode': 200,
            'body': json.dumps('Student record added successfully')
        }

    elif event['httpMethod'] == 'GET':
        # Fetch student record by student_id
        student_id = event['queryStringParameters']['student_id']
        response = table.get_item(Key={'student_id': student_id})
        return {
            'statusCode': 200,
            'body': json.dumps(response.get('Item', 'Record not found'))
        }

    elif event['httpMethod'] == 'PUT':
        # Update student details
        student = json.loads(event['body'])
        student_id = student['student_id']

        # Update the attributes (example: updating name and course)
        table.update_item(
            Key={'student_id': student_id},
            UpdateExpression="SET #name = :name, #course = :course",
            ExpressionAttributeNames={
                '#name': 'name',
                '#course': 'course'
            },
            ExpressionAttributeValues={
                ':name': student['name'],
                ':course': student['course']
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Student record updated successfully')
        }

    elif event['httpMethod'] == 'DELETE':
        # Delete student record by student_id
        student_id = event['queryStringParameters']['student_id']
        table.delete_item(Key={'student_id': student_id})
        return {
            'statusCode': 200,
            'body': json.dumps('Student record deleted successfully')
        }

    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Unsupported method')
        }