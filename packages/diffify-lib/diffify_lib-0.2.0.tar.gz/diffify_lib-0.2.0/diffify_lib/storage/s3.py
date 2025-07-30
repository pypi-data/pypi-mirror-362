"""
Classes for connecting to, reading from and writing to an Amazon S3 bucket
"""

import gzip
import json
import logging
import time
from typing import List, Optional, Union

import boto3
from botocore.exceptions import ClientError


class S3Connector:
    """A class to hold a client connection to S3 services"""

    def __init__(self, key: str, secret: str, s3_params: dict) -> None:
        """

        :type key: str
        :param key: Access key to use when creating the client.
        :type secret: str
        :param secret: The secret to use when creating the client.
        :type s3_params: dict
        :param s3_params: Other key word arguments relevant to the client connection.
          See :py:meth:`boto3.session.Session.client`
        """
        if not s3_params:
            raise ValueError(
                "s3_params should be a dictionary with fields 'region_name',"
                + " 'endpoint_url', 'service_name'"
            )

        self.client = boto3.client(
            aws_access_key_id=key, aws_secret_access_key=secret, **s3_params
        )


class S3Reader:
    """A class for objects that read data from a specific S3 bucket"""

    def __init__(
        self, conn: S3Connector, bucket: str, logger: Optional[logging.Logger] = None
    ) -> None:
        """
        :type conn: diffify.s3.S3Connector
        :param conn: Object that provides a client connection to S3 service.
        :type bucket: str
        :param bucket: Name of the S3 bucket to read from
        :type logger: logging.Logger
        :param logger: An object for writing to the application log file.
        """
        self.conn = conn
        self.bucket = bucket
        self.logger = logger

    def read(self, key: str) -> list:
        """Reads the contents of a json file in the bucket as a list

        :param key: the name of the json file in the bucket. Respects file-path like
          names e.g "packages/packages-versions.json". If this ends with ".gz", the
          data will be decompressed on reading.
        """
        if self.logger:
            self.logger.info(f"Reading data from {key}")

        obj = self.conn.client.get_object(Bucket=self.bucket, Key=key)
        content = obj["Body"].read()
        if key.endswith(".gz"):
            content = gzip.decompress(content)

        return json.loads(content)


class S3Writer:
    """A class for objects that write data to a specific S3 bucket"""

    def __init__(
        self,
        conn: S3Connector,
        bucket: str,
        acl_policy: str = "private",
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
        :type conn: diffify.s3.S3Connector
        :param conn: Object that provides a client connection to S3 service.
        :type bucket: str
        :param bucket: Name of the S3 bucket to write to
        :type acl_policy:
        :param acl_policy: access control, see
          https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html
        :type logger: logging.Logger
        :param logger: An object for writing to the application log file.
        """
        self.conn = conn
        self.bucket = bucket
        self.acl_policy = acl_policy
        self.logger = logger

    def write(
        self, obj: Union[dict, List[str], List[dict]], key: str, compress: bool = False
    ):
        """Writes a dictionary object to an object in the S3 bucket

        Dictionary objects are written as UTF-8 encoded json files.
        If the 'compress' option is passed, objects are written as gzipped UTF-8
        encoded json.gz files.

        :type obj: dict
        :param obj: A dictionary of data to write to file
        :type key: str
        :param key: The name of the asset in the bucket. Respects file-path like
          names, e.g "packages/packages-versions.json"
        :type compress: bool
        :param compress: Whether to write the data in compressed format or not
        """
        if self.logger:
            self.logger.info(f"Writing data to {key}")

        contents = bytes(json.dumps(obj, default=str).encode("UTF-8"))
        if compress:
            contents = gzip.compress(contents)
            try:
                put = self.conn.client.put_object(
                    Bucket=self.bucket,
                    Key=key,
                    Body=contents,
                    ContentType="application/json",
                    ContentEncoding="gzip",
                    ACL=self.acl_policy,
                )
            except ClientError as e:
                response = e.response["Error"]["Code"]
                if self.logger:
                    self.logger.info(
                        f"Can't write to {key} with {response} error,"
                        + " pause and try again"
                    )
                # wait then try to write content again
                time.sleep(10)
                put = self.conn.client.put_object(
                    Bucket=self.bucket,
                    Key=key,
                    Body=contents,
                    ContentType="application/json",
                    ContentEncoding="gzip",
                    ACL=self.acl_policy,
                )
        else:
            try:
                put = self.conn.client.put_object(
                    Bucket=self.bucket,
                    Key=key,
                    Body=contents,
                    ContentType="application/json",
                    ACL=self.acl_policy,
                )
            except ClientError as e:
                response = e.response["Error"]["Code"]
                if self.logger:
                    self.logger.info(
                        f"Can't write to {key} with {response} error,"
                        + " pause and try again"
                    )
                # wait then try to write content again
                time.sleep(10)
                put = self.conn.client.put_object(
                    Bucket=self.bucket,
                    Key=key,
                    Body=contents,
                    ContentType="application/json",
                    ACL=self.acl_policy,
                )
        return put
