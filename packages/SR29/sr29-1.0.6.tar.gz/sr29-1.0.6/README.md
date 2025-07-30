Description
===========
  this program for protect your file or script with encode SR29

INSTALL
-------
  instaling using pip
  ```sh
  pip install SR29
  ```

# Python
  ## for encode
  ```python
  import sr29
  encode = sr29.encrypt('string', 'password', salt='I Love You').hexdigest()
  print(encode)
  ```

  ## for decode
  ```python
  decode = sr29.decrypt(encode, 'password', salt='I Love You')
  print(decode)
  ```
# Program Script
  ```sh
  $ SR29 fileIn.txt -o fileOut.txt -p Your_Password -s "I Love Python" --progress
  ```
