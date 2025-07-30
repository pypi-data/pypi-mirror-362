from datetime import timedelta

from app import app
from wedeliver_core_plus.helpers.amazon.get_s3_client import get_s3_client


def get_file_url(s3_path, expiration_minutes=30, s3_client=None):
    """
    Upload a file to an S3 bucket
    """
    # return s3_path

    if not s3_path:
        return s3_path

    if not s3_path.startswith("http"):
        s3_path = "https://{}/{}".format(app.config.get("S3_BUCKET"), s3_path)

    path_parts = s3_path.replace("https://", "").split("/")
    bucket = path_parts.pop(0).split(".").pop(0)
    key = "/".join(path_parts)

    response = None
    # s3_client = None
    try:
        s3_client = s3_client or get_s3_client()
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=int(timedelta(minutes=expiration_minutes).total_seconds()),
        )
    except Exception as e:
        app.logger.error(str(e))

    # The response contains the presigned URL
    app.logger.debug(response)
    return response


def get_file_url_bulk(list_dict, key_name, s3_client=None):
    """
    This function will append plain url to list of dictionaries
    :param list_dict: list of dictionaries
    :param key_name: key name to append plain url to
    :param s3_client: s3 client
    :return: list of dictionaries
    """
    s3_client = s3_client or get_s3_client()
    for item in list_dict:
        item[key_name] = get_file_url(item.get(key_name), s3_client=s3_client)
    return list_dict

if __name__ == "__main__":
    url = get_file_url(
        s3_path="owner_national_attachment/1660823074_ihbxlpymqxxjuzrqom.jpe"
        # s3_path="https://dev-wedeliver-slips.s3.eu-west-1.amazonaws.com/development/PS/images/cad3b9038e021648.jpg"
    )
    test = url
